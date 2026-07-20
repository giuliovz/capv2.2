from filtros.comercial import imovel_interessante


class Imovel:
    def __init__(self, tipo, quartos, valor):
        self.tipo = tipo
        self.quartos = quartos
        self.valor = valor


def test_imovel_interessante_permite_tipo_casa_e_apartamento():
    imovel = Imovel("Apartamento", 3, 500000)

    assert imovel_interessante(imovel) is True


def test_imovel_interessante_rejeita_tipo_nao_permitido():
    imovel = Imovel("Terreno", 3, 500000)

    assert imovel_interessante(imovel) is False


def test_imovel_interessante_rejeita_quartos_menos_que_dois():
    imovel = Imovel("Apartamento", 1, 400000)

    assert imovel_interessante(imovel) is False


def test_imovel_interessante_rejeita_valor_acima_do_limite():
    imovel = Imovel("Casa", 3, 900000)

    assert imovel_interessante(imovel) is False
