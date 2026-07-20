from modelos.imovel import Imovel
from processamento.higienizacao import _titulo_generico, _titulo_por_link
from processamento.pipeline import _imovel_invalido


def test_titulo_generico_detecta_variacoes():
    assert _titulo_generico("") is True
    assert _titulo_generico("Ir para o conteúdo") is True
    assert _titulo_generico("Sem título") is True
    assert _titulo_generico("Apartamento no Centro") is False


def test_titulo_por_link_imoblu_e_zelt():
    t1 = _titulo_por_link("IMOBLU", "https://imoblu.com.br/imovel/?id=503902")
    t2 = _titulo_por_link(
        "ZELT",
        "https://www.zelt.com.br/imovel/apartamento-blumenau-2-quartos-90-m/AP6358-ZLTA",
    )

    assert "503902" in t1
    assert "Apartamento Blumenau" in t2


def test_imovel_invalido_quando_apenas_placeholder():
    imovel = Imovel(
        portal="IMOBLU",
        link="https://imoblu.com.br/imovel/?id=503902",
        titulo="Ir para o conteúdo",
        bairro="",
        valor=0,
        quartos=0,
    )

    assert _imovel_invalido(imovel) is True


def test_imovel_valido_nao_descarta():
    imovel = Imovel(
        portal="ZELT",
        link="https://www.zelt.com.br/imovel/sala-blumenau-47-m/SA0724-ZLTA",
        titulo="Sala Blumenau",
        bairro="Velha",
        valor=2210,
        quartos=0,
    )

    assert _imovel_invalido(imovel) is False
