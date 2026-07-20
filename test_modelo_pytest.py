from modelos.imovel import Imovel


def test_imovel_to_dict_contains_fields():
    imovel = Imovel(
        portal="Teste",
        link="https://teste.com",
        tipo="Casa",
        finalidade="Venda",
        bairro="Tribess",
        cidade="Blumenau",
        valor=390000,
        quartos=3,
        suites=0,
        banheiros=1,
        vagas=1,
        area=120.0,
        area_privativa=110.0,
        area_total=120.0,
        data_captura="2026-07-18",
        status="Ativo",
        descricao="Descrição teste",
        pontuacao=80,
        classificacao="Excelente"
    )

    dados = imovel.to_dict()

    assert dados["portal"] == "Teste"
    assert dados["tipo"] == "Casa"
    assert dados["finalidade"] == "Venda"
    assert dados["area_privativa"] == 110.0
    assert dados["area_total"] == 120.0
    assert dados["classificacao"] == "Excelente"


def test_para_dict_alias_matches_to_dict():
    imovel = Imovel()

    assert imovel.para_dict() == imovel.to_dict()
