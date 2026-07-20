from exportacao.excel import exportar_excel
from modelos.imovel import Imovel
import os


def test_exportar_excel_creates_file(tmp_path):
    imovel = Imovel(
        portal="ZELT",
        link="https://teste.com",
        tipo="Apartamento",
        bairro="Centro",
        cidade="Blumenau",
        valor=450000,
        quartos=3,
        area_privativa=120,
        area_total=120,
        descricao="Descrição de teste"
    )

    arquivo = exportar_excel([imovel])

    assert arquivo.exists()
    assert arquivo.parent.name == "relatorios"
