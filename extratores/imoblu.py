import re

from modelos.imovel import Imovel
from extratores.base import ExtratorBase


class ExtratorImoblu(ExtratorBase):

    def extrair(self, texto, link):

        valor = 0

        valores = re.findall(
            r"R\$\s?([\d\.]+)",
            texto
        )

        if valores:
            valor = int(
                valores[0]
                .replace(".", "")
            )

        quartos = 0

        encontrados = re.findall(
            r"(\d+)\s+quartos?",
            texto.lower()
        )

        if encontrados:
            quartos = int(
                encontrados[0]
            )

        titulo = ""

        linhas = texto.split("\n")

        if linhas:
            titulo = linhas[0][:150]

        return Imovel(
            portal="IMOBLU",
            link=link,
            titulo=titulo,
            valor=valor,
            quartos=quartos,
            descricao=texto[:500]
        )