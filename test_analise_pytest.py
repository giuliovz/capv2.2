from analise.ia import analisar_imovel, opinar_top_imovel
from modelos.imovel import Imovel


def test_analisar_imovel_gera_pontuacao_e_classificacao():
    imovel = Imovel(
        tipo="Apartamento",
        bairro="Centro",
        valor=450000,
        quartos=3,
        descricao="Excelente apartamento novo, bem localizado, com garagem e vista.",
    )

    pontos, classificacao = analisar_imovel(imovel)

    assert pontos >= 70
    assert classificacao == "Excelente"


def test_opinar_top_imovel_retorna_resumo_textual():
    texto = opinar_top_imovel(
        titulo="Apartamento Centro",
        bairro="Centro",
        valor=580000,
        pontuacao=82,
        classificacao="Excelente",
        portal="ZELT",
    )

    assert "Apartamento Centro" in texto
    assert "Recomendação" in texto
    assert "Base da análise" in texto


def test_opinar_top_imovel_aceita_tons():
    base = {
        "titulo": "Casa Vila Nova",
        "bairro": "Vila Nova",
        "valor": 890000,
        "pontuacao": 70,
        "classificacao": "Boa",
        "portal": "ARLETE",
    }

    t1 = opinar_top_imovel(**base, tom="conservador")
    t2 = opinar_top_imovel(**base, tom="equilibrado")
    t3 = opinar_top_imovel(**base, tom="agressivo")

    assert "conservadora" in t1.lower()
    assert "abordagem comercial prioritária" in t2.lower()
    assert "agressiva" in t3.lower()
