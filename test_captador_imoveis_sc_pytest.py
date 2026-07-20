from captadores.imoveis_sc import CaptadorImoveisSC
from processamento.pipeline import _criar_imovel_estruturado


def test_captador_imoveis_sc_extrai_imovel_e_monta_link():
    html = r'''
    <script>self.__next_f.push([1,"property":{"id":5135561,"codigo":"AP0633","slug":"apartamento-com-2-dormitorios-sendo-1-suite-78-m2-por-r-699-000-fortaleza-blumenau-sc-5135561","titulo":"Apartamento com 2 dormitórios sendo 1 suíte, 78 m² por R$ 699.000 - Fortaleza - Blumenau/SC","preco":699000,"quartos":2,"suites":1,"vagas":2,"banheiros":2,"area_util":78,"area_total":108,"bairro":"Fortaleza","slug_bairro":"fortaleza","cidade":"Blumenau","slug_cidade":"blumenau","slug_tipo_negocio":"comprar","nome_tipo_negocio":"Venda","slug_tipo_imovel":"apartamento","nome_tipo_imovel":"Apartamento","nome_anunciante":"Ana Cota Imóveis","nome_regiao":"Vale Europeu","localizacao_aproximada_lng":null}])</script>
    '''

    captador = CaptadorImoveisSC()
    imoveis = captador._extrair_imoveis_html(html)

    assert len(imoveis) == 1
    assert imoveis[0]["codigo"] == "AP0633"

    link = captador._montar_link(imoveis[0])
    assert link == "https://www.imoveis-sc.com.br/blumenau/comprar/apartamento/fortaleza/apartamento-com-2-dormitorios-sendo-1-suite-78-m2-por-r-699-000-fortaleza-blumenau-sc-5135561.html"


def test_captador_imoveis_sc_monta_url_com_configuracao():
    captador = CaptadorImoveisSC(cidade="joinville", tipo_negocio="alugar", max_paginas=3)

    assert captador.url == "https://www.imoveis-sc.com.br/joinville/alugar"
    assert captador._montar_url_pagina(1) == "https://www.imoveis-sc.com.br/joinville/alugar"
    assert captador._montar_url_pagina(3) == "https://www.imoveis-sc.com.br/joinville/alugar?page=3"


def test_captador_imoveis_sc_pagina_e_para_em_pagina_repetida(monkeypatch):
    captador = CaptadorImoveisSC(max_paginas=4)

    html_pagina_1 = r'''
    <script>{"id":1,"codigo":"A1","slug":"imovel-1","titulo":"Imóvel 1","preco":100000,"quartos":2,"suites":1,"vagas":1,"banheiros":2,"area_util":80,"area_total":100,"bairro":"Velha","slug_bairro":"velha","cidade":"Blumenau","slug_cidade":"blumenau","slug_tipo_negocio":"comprar","nome_tipo_negocio":"Venda","slug_tipo_imovel":"apartamento","nome_tipo_imovel":"Apartamento","nome_anunciante":"Teste","nome_regiao":"Vale","localizacao_aproximada_lng":null}</script>
    <script>{"id":2,"codigo":"A2","slug":"imovel-2","titulo":"Imóvel 2","preco":120000,"quartos":3,"suites":1,"vagas":2,"banheiros":2,"area_util":90,"area_total":110,"bairro":"Velha","slug_bairro":"velha","cidade":"Blumenau","slug_cidade":"blumenau","slug_tipo_negocio":"comprar","nome_tipo_negocio":"Venda","slug_tipo_imovel":"casa","nome_tipo_imovel":"Casa","nome_anunciante":"Teste","nome_regiao":"Vale","localizacao_aproximada_lng":null}</script>
    '''
    html_pagina_2 = r'''
    <script>{"id":3,"codigo":"A3","slug":"imovel-3","titulo":"Imóvel 3","preco":140000,"quartos":2,"suites":0,"vagas":1,"banheiros":1,"area_util":70,"area_total":85,"bairro":"Centro","slug_bairro":"centro","cidade":"Blumenau","slug_cidade":"blumenau","slug_tipo_negocio":"comprar","nome_tipo_negocio":"Venda","slug_tipo_imovel":"apartamento","nome_tipo_imovel":"Apartamento","nome_anunciante":"Teste","nome_regiao":"Vale","localizacao_aproximada_lng":null}</script>
    '''

    respostas = {
        captador._montar_url_pagina(1): html_pagina_1,
        captador._montar_url_pagina(2): html_pagina_2,
        captador._montar_url_pagina(3): html_pagina_2,
    }

    monkeypatch.setattr(captador, "_baixar_html", lambda url: respostas[url])

    resultados = captador.capturar()

    assert len(resultados) == 3
    assert [item["link"] for item in resultados] == [
        "https://www.imoveis-sc.com.br/blumenau/comprar/apartamento/velha/imovel-1.html",
        "https://www.imoveis-sc.com.br/blumenau/comprar/casa/velha/imovel-2.html",
        "https://www.imoveis-sc.com.br/blumenau/comprar/apartamento/centro/imovel-3.html",
    ]


def test_pipeline_cria_imovel_estruturado_para_imoveis_sc():
    anuncio = {
        "portal": "IMOVEIS_SC",
        "link": "https://www.imoveis-sc.com.br/blumenau/comprar/apartamento/fortaleza/imovel-1.html",
        "dados_imovel": {
            "codigo": "AP0633",
            "titulo": "Apartamento com 2 dormitórios sendo 1 suíte",
            "preco": 699000,
            "quartos": 2,
            "suites": 1,
            "vagas": 2,
            "banheiros": 2,
            "area_util": 78,
            "area_total": 108,
            "bairro": "Fortaleza",
            "cidade": "Blumenau",
            "nome_tipo_negocio": "Venda",
            "nome_tipo_imovel": "Apartamento",
            "nome_anunciante": "Ana Cota Imóveis",
            "nome_regiao": "Vale Europeu",
        },
    }

    imovel = _criar_imovel_estruturado(anuncio)

    assert imovel is not None
    assert imovel.portal == "IMOVEIS_SC"
    assert imovel.codigo == "AP0633"
    assert imovel.valor == 699000
    assert imovel.quartos == 2
    assert imovel.area_privativa == 78
    assert "Anunciante: Ana Cota Imóveis" in imovel.descricao