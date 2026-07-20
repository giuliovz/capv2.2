import argparse
import os
import socket
import subprocess
import sys
import webbrowser

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inicia o dashboard web")
    parser.add_argument("--host", default=os.getenv("SITE_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("SITE_PORT", "8000")))
    parser.add_argument("--open", action="store_true", help="Abre o dashboard no navegador")
    parser.add_argument("--background", action="store_true", help="Inicia em segundo plano e libera o terminal")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    porta_escolhida = _selecionar_porta(args.port)
    if porta_escolhida != args.port:
        print(f"Porta {args.port} em uso. Iniciando em {porta_escolhida}.")

    url_dashboard = f"http://127.0.0.1:{porta_escolhida}/dashboard"

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
        print(f"Servidor iniciado em segundo plano (PID {proc.pid}).")
        print(f"Dashboard disponível em: {url_dashboard}")
        sys.exit(0)

    print(f"Dashboard disponível em: {url_dashboard}")
    print("Servidor ativo. Para encerrar, pressione CTRL+C.")

    if args.open:
        try:
            webbrowser.open(url_dashboard)
        except Exception:
            pass

    iniciar_servidor(host=args.host, port=porta_escolhida)
