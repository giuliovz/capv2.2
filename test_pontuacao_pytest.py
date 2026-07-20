from filtros.pontuacao import calcular_pontuacao, classificar


class Imovel:
    def __init__(self, tipo, quartos, valor, bairro, descricao):
        self.tipo = tipo
        self.quartos = quartos
        self.valor = valor
        self.bairro = bairro
        self.descricao = descricao


def test_calcular_pontuacao_tipo_e_quartos():
    imovel = Imovel("Apartamento", 3, 450000, "Centro", "Apartamento amplo")

    assert calcular_pontuacao(imovel) >= 65


def test_classificar_retorna_excellent_para_pontuacao_alta():
    assert classificar(85) == "Excelente"


def test_classificar_retorna_media_para_pontuacao_media():
    assert classificar(45) == "Média"
