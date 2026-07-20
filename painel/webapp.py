from datetime import datetime
from threading import Lock, Thread
from pathlib import Path
import subprocess
import sys

from flask import Flask, jsonify, request, send_file

from app import preparar_pastas
from config import BASE_DIR, RELATORIOS_DIR
from painel.html_dashboard import gerar_html_dashboard
from processamento.pipeline import executar_pipeline


app = Flask(__name__)
_PORTA_ATUAL = 8000


def _progresso_inicial():
    return {
        "etapa": "captura",
        "percentual": 0,
        "mensagem": "Aguardando início.",
        "etapas": [
            {"nome": "captura", "status": "pendente"},
            {"nome": "extracao", "status": "pendente"},
            {"nome": "classificacao", "status": "pendente"},
            {"nome": "exportacao", "status": "pendente"},
            {"nome": "dashboard", "status": "pendente"},
        ],
    }

_estado_lock = Lock()
_estado_captura = {
    "status": "ocioso",
    "mensagem": "Pronto para iniciar.",
    "inicio": None,
    "fim": None,
    "resumo": None,
    "erro": None,
    "progresso": _progresso_inicial(),
    "tom_ia": "equilibrado",
}

_tons_permitidos = {"conservador", "equilibrado", "agressivo"}


def _porta_livre(porta):
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex(("127.0.0.1", porta)) != 0


def _proxima_porta_livre(base=8000, tentativas=40, evitar=None):
    evitar = evitar or set()
    for porta in range(base, base + tentativas):
        if porta in evitar:
            continue
        if _porta_livre(porta):
            return porta
    return None


def _set_estado(**kwargs):
    with _estado_lock:
        _estado_captura.update(kwargs)


def _get_estado():
    with _estado_lock:
        return dict(_estado_captura)


def _executar_em_background():
    estado_atual = _get_estado()
    tom_ia_atual = estado_atual.get("tom_ia", "equilibrado")

    progresso = _progresso_inicial()
    progresso["mensagem"] = "Iniciando pipeline..."

    _set_estado(
        status="executando",
        mensagem="Captura em execução...",
        inicio=datetime.now().isoformat(),
        fim=None,
        resumo=None,
        erro=None,
        progresso=progresso,
    )

    try:
        def callback_progresso(payload):
            _set_estado(progresso=payload)

        resumo = executar_pipeline(progress_callback=callback_progresso, tom_ia=tom_ia_atual)

        progresso_final = {
            "etapa": "dashboard",
            "percentual": 100,
            "mensagem": "Pipeline concluído.",
            "etapas": [
                {"nome": "captura", "status": "concluida"},
                {"nome": "extracao", "status": "concluida"},
                {"nome": "classificacao", "status": "concluida"},
                {"nome": "exportacao", "status": "concluida"},
                {"nome": "dashboard", "status": "concluida"},
            ],
        }

        _set_estado(
            status="concluido",
            mensagem="Captura concluída com sucesso.",
            fim=datetime.now().isoformat(),
            resumo=resumo,
            erro=None,
            progresso=progresso_final,
        )
    except Exception as erro:
        _set_estado(
            status="erro",
            mensagem="Falha durante a captura.",
            fim=datetime.now().isoformat(),
            resumo=None,
            erro=str(erro),
            progresso={
                "etapa": "dashboard",
                "percentual": 100,
                "mensagem": "Pipeline finalizado com erro.",
                "etapas": [
                    {"nome": "captura", "status": "concluida"},
                    {"nome": "extracao", "status": "concluida"},
                    {"nome": "classificacao", "status": "concluida"},
                    {"nome": "exportacao", "status": "concluida"},
                    {"nome": "dashboard", "status": "erro"},
                ],
            },
        )


@app.get("/")
def home():
    tom = _get_estado().get("tom_ia", "equilibrado")
    caminho = gerar_html_dashboard(tom_ia=tom)
    return send_file(caminho)


@app.get("/dashboard")
def dashboard():
    caminho = RELATORIOS_DIR / "dashboard.html"
    tom = _get_estado().get("tom_ia", "equilibrado")
    caminho = gerar_html_dashboard(caminho, tom_ia=tom)
    return send_file(caminho)


@app.post("/api/captura/iniciar")
def iniciar_captura():
    estado = _get_estado()
    if estado["status"] == "executando":
        return jsonify({"ok": False, "mensagem": "Já existe uma captura em execução."}), 409

    thread = Thread(target=_executar_em_background, daemon=True)
    thread.start()
    return jsonify({"ok": True, "mensagem": "Captura iniciada."})


@app.get("/api/captura/status")
def status_captura():
    return jsonify(_get_estado())


@app.get("/api/server/info")
def server_info():
    return jsonify(
        {
            "porta_atual": _PORTA_ATUAL,
            "url_dashboard": f"http://127.0.0.1:{_PORTA_ATUAL}/dashboard",
        }
    )


@app.post("/api/server/nova-porta")
def server_nova_porta():
    porta = _proxima_porta_livre(base=max(8000, _PORTA_ATUAL), evitar={_PORTA_ATUAL})
    if not porta:
        return jsonify({"ok": False, "mensagem": "Não foi possível encontrar uma porta livre."}), 500

    comando = [sys.executable, str(BASE_DIR / "executar_site.py"), "--port", str(porta)]

    try:
        subprocess.Popen(
            comando,
            cwd=str(BASE_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception as erro:
        return jsonify({"ok": False, "mensagem": f"Falha ao iniciar nova instância: {erro}"}), 500

    return jsonify(
        {
            "ok": True,
            "porta": porta,
            "url_dashboard": f"http://127.0.0.1:{porta}/dashboard",
            "mensagem": "Nova instância iniciada em outra porta.",
        }
    )


@app.get("/api/ia/tom")
def obter_tom_ia():
    tom = _get_estado().get("tom_ia", "equilibrado")
    return jsonify({"tom": tom, "opcoes": sorted(_tons_permitidos)})


@app.post("/api/ia/tom")
def definir_tom_ia():
    payload = request.get_json(silent=True) or {}
    tom = (payload.get("tom") or "").strip().lower()

    if tom not in _tons_permitidos:
        return jsonify({"ok": False, "mensagem": "Tom inválido. Use: conservador, equilibrado ou agressivo."}), 400

    estado = _get_estado()
    if estado.get("status") == "executando":
        return jsonify({"ok": False, "mensagem": "Aguarde o término da captura para alterar o tom."}), 409

    _set_estado(tom_ia=tom)
    gerar_html_dashboard(tom_ia=tom)
    return jsonify({"ok": True, "tom": tom, "mensagem": "Tom da IA atualizado."})


def iniciar_servidor(host="0.0.0.0", port=8000):
    global _PORTA_ATUAL
    _PORTA_ATUAL = int(port)

    preparar_pastas()
    tom = _get_estado().get("tom_ia", "equilibrado")
    gerar_html_dashboard(tom_ia=tom)
    app.run(host=host, port=port)


if __name__ == "__main__":
    iniciar_servidor()