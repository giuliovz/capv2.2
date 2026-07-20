from extratores.zelt import ExtratorZelt
from extratores.arlete import ExtratorArlete


def test_extrator_zelt_parses_valor_e_quartos():
    texto = """
    Apartamento Blumenau
    3 quartos
    R$ 450.000
    120 m²
    """

    extrator = ExtratorZelt()
    imovel = extrator.extrair(texto, "https://teste.com")

    dados = imovel.para_dict()

    assert dados["valor"] == 450000
    assert dados["quartos"] == 3
    assert dados["link"] == "https://teste.com"


def test_extrator_zelt_defaults_missing_fields():
    texto = """
    Apartamento
    """

    extrator = ExtratorZelt()
    imovel = extrator.extrair(texto, "https://teste.com")

    dados = imovel.para_dict()

    assert dados["valor"] == 0
    assert dados["quartos"] == 0


def test_extrator_arlete_parses_valor_e_quartos():
    texto = """
    Casa para venda em Blumenau
    4 quartos
    2 vagas
    R$ 1.250.000
    210 m²
    """

    extrator = ExtratorArlete()
    imovel = extrator.extrair(texto, "https://arletegaldinocorretora.com.br/imovel/123")

    dados = imovel.para_dict()

    assert dados["valor"] == 1250000
    assert dados["quartos"] == 4
    assert dados["vagas"] == 2
    assert dados["portal"] == "ARLETE"


def test_extrator_arlete_guarda_links_de_imagem_imogestao_na_descricao():
    texto = """
    Apartamento para venda em Blumenau
    2 quartos
    R$ 650.000

    IMAGENS_IMOGESTAO:
    https://sistema.imogestao.com.br/fotos/592/1.jpg
    https://sistema.imogestao.com.br/fotos/592/2.jpg
    """

    extrator = ExtratorArlete()
    imovel = extrator.extrair(texto, "https://arletegaldinocorretora.com.br/imovel/apto-1")
    dados = imovel.para_dict()

    assert "Imagens (ImoGestao):" in dados["descricao"]
    assert "https://sistema.imogestao.com.br/fotos/592/1.jpg" in dados["descricao"]
