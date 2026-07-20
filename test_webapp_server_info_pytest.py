from painel import webapp


def test_server_info_usa_host_publico_da_requisicao():
    with webapp.app.test_client() as client:
        resposta = client.get(
            "/api/server/info",
            headers={
                "Host": "127.0.0.1:8020",
                "X-Forwarded-Host": "ubiquitous-space-orbit-r77wqj6rpg96cxp9-8020.app.github.dev",
                "X-Forwarded-Proto": "https",
            },
        )

    assert resposta.status_code == 200
    payload = resposta.get_json()
    assert payload["url_dashboard"] == "https://ubiquitous-space-orbit-r77wqj6rpg96cxp9-8000.app.github.dev/dashboard"


def test_nova_porta_retorna_url_publica_com_porta_nova(monkeypatch):
    monkeypatch.setattr(webapp, "_PORTA_ATUAL", 8020)
    monkeypatch.setattr(webapp, "_proxima_porta_livre", lambda base=8000, tentativas=40, evitar=None: 8021)

    class DummyProc:
        pass

    monkeypatch.setattr(webapp.subprocess, "Popen", lambda *args, **kwargs: DummyProc())

    with webapp.app.test_client() as client:
        resposta = client.post(
            "/api/server/nova-porta",
            headers={
                "Host": "127.0.0.1:8020",
                "X-Forwarded-Host": "ubiquitous-space-orbit-r77wqj6rpg96cxp9-8020.app.github.dev",
                "X-Forwarded-Proto": "https",
            },
        )

    assert resposta.status_code == 200
    payload = resposta.get_json()
    assert payload["ok"] is True
    assert payload["porta"] == 8021
    assert payload["url_dashboard"] == "https://ubiquitous-space-orbit-r77wqj6rpg96cxp9-8021.app.github.dev/dashboard"