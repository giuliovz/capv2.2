import argparse
import http.client
import os
import signal
import socket
import subprocess
import sys
import time
import webbrowser
from threading import Thread

from painel.webapp import iniciar_servidor


def _porta_livre(porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex(("127.0.0.1", porta)) != 0


def _selecionar_porta(preferida, tentativas=20):
    for porta in range(preferida, preferida + tentativas):
        if _porta_livre(porta):
            return porta
    raise RuntimeError("Não foi encontrada porta livre para iniciar o site.")


def _encerrar_instancias_antigas():
    """Mata processos anteriores de executar_site.py (exceto o próprio processo)."""
    proprio_pid = os.getpid()
    script = os.path.abspath(__file__)
    mortos = []

    try:
        saida = subprocess.check_output(
            ["ps", "aux"], text=True, stderr=subprocess.DEVNULL
        )
        for linha in saida.splitlines():
            if "executar_site" not in linha:
                continue
            partes = linha.split()
            if len(partes) < 2:
                continue
            try:
                pid = int(partes[1])
            except ValueError:
                continue
            if pid == proprio_pid:
                continue
            try:
                os.kill(pid, signal.SIGTERM)
                mortos.append(pid)
            except ProcessLookupError:
                pass
            except PermissionError:
                pass

    except Exception:
        pass

    if mortos:
        time.sleep(0.5)
        for pid in mortos:
            try:
                os.kill(pid, signal.SIGKILL)
            except Exception:
                pass
        print(f"Instâncias anteriores encerradas: {mortos}")


def _url_publica(porta):
    codespace = os.getenv("CODESPACE_NAME")
    dominio = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
    if codespace and dominio:
        return f"https://{codespace}-{porta}.{dominio}/dashboard"
    return f"http://127.0.0.1:{porta}/dashboard"


def _aguardar_servidor(host, porta, timeout=15):
    inicio = time.time()
    host_http = "127.0.0.1" if host in {"0.0.0.0", "::", ""} else host

    while time.time() - inicio < timeout:
        try:
            conn = http.client.HTTPConnection(host_http, porta, timeout=1)
            conn.request("GET", "/api/server/info")
            resposta = conn.getresponse()
            resposta.read()
            conn.close()
            if resposta.status == 200:
                return True
        except Exception:
            pass

        time.sleep(0.25)

    return False


def _abrir_quando_pronto(url, host, porta, timeout=15):
    if _aguardar_servidor(host, porta, timeout=timeout):
        try:
            webbrowser.open(url)
        except Exception:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inicia o dashboard web")
    parser.add_argument("--host", default=os.getenv("SITE_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("SITE_PORT", "8000")))
    parser.add_argument("--open", action="store_true", help="Abre o dashboard no navegador")
    parser.add_argument("--background", action="store_true", help="Inicia em segundo plano e libera o terminal")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if not args.worker:
        _encerrar_instancias_antigas()

    porta_escolhida = _selecionar_porta(args.port)
    if porta_escolhida != args.port:
        print(f"Porta {args.port} em uso. Iniciando em {porta_escolhida}.")

    url_dashboard = _url_publica(porta_escolhida)

    if args.background and not args.worker:
        comando = [
            sys.executable,
            __file__,
            "--host",
            args.host,
            "--port",
            str(porta_escolhida),
            "--worker",
        ]
        proc = subprocess.Popen(
            comando,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

        if not _aguardar_servidor(args.host, porta_escolhida, timeout=20):
            if proc.poll() is not None:
                print("Falha ao iniciar o servidor em segundo plano.")
                sys.exit(1)

        if args.open:
            try:
                webbrowser.open(url_dashboard)
            except Exception:
                pass

        print(f"Servidor iniciado em segundo plano (PID {proc.pid}).")
        print(f"Dashboard disponível em: {url_dashboard}")
        sys.exit(0)

    print(f"Dashboard disponível em: {url_dashboard}")
    print("Servidor ativo. Para encerrar, pressione CTRL+C.")

    if args.open:
        Thread(
            target=_abrir_quando_pronto,
            args=(url_dashboard, args.host, porta_escolhida),
            daemon=True,
        ).start()

    iniciar_servidor(host=args.host, port=porta_escolhida)
