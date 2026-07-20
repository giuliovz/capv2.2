from modelos.imovel import Imovel
from processamento.qualidade import avaliar_imovel


def test_avaliar_imovel_bom_score_alto():
    imovel = Imovel(
        titulo="Apartamento Centro",
        bairro="Centro",
        valor=650000,
        quartos=3,
        descricao="Apartamento amplo com excelente localizacao, duas vagas e condominio completo para familia.",
    )

    resultado = avaliar_imovel(imovel)

    assert resultado.score >= 70
    assert resultado.bloquear is False


def test_avaliar_imovel_fraco_bloqueia():
    imovel = Imovel(
        titulo="Ir para o conteúdo",
        bairro="",
        valor=0,
        quartos=0,
        descricao="curta",
    )

    resultado = avaliar_imovel(imovel)

    assert resultado.score < 35
    assert resultado.bloquear is True
    assert "bairro_ausente" in resultado.motivos
