from pathlib import Path

from captadores.arlete import CaptadorArlete


def test_validar_links_fallback_relatorio():
    captador = CaptadorArlete()

    linhas = [
        "# comentario",
        "",
        "abc",
        "https://google.com/imovel/1",
        "https://sistema.imogestao.com.br/fotos/592/1.jpg",
        "https://arletegaldinocorretora.com.br/imoveis?pretensao=comprar",
        "https://arletegaldinocorretora.com.br/imovel/casa-1",
        "https://arletegaldinocorretora.com.br/imovel/casa-1",
        "http://arletegaldinocorretora.com.br/imovel/apto-2",
    ]

    links_validos, relatorio = captador._validar_links_fallback(linhas)

    assert len(links_validos) == 2
    assert relatorio["lidas"] == 9
    assert relatorio["comentarios_ou_vazias"] == 2
    assert relatorio["aceitos"] == 2
    assert relatorio["rejeitados"] == 5
    assert relatorio["rejeitados_formato"] == 1
    assert relatorio["rejeitados_dominio"] == 2
    assert relatorio["rejeitados_rota"] == 1
    assert relatorio["rejeitados_duplicado"] == 1


def test_salvar_links_limpos_reescreve_arquivo(tmp_path):
    captador = CaptadorArlete()
    caminho = tmp_path / "arlete_links.txt"

    links_validos = [
        "https://arletegaldinocorretora.com.br/imovel/casa-1",
        "https://arletegaldinocorretora.com.br/imovel/apto-2",
    ]

    captador._salvar_links_limpos(caminho, links_validos)

    texto = Path(caminho).read_text(encoding="utf-8")
    assert "apenas links válidos e únicos" in texto
    assert links_validos[0] in texto
    assert links_validos[1] in texto
