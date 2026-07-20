import json
import re
from urllib.request import Request, urlopen

from captadores.base import CaptadorBase
from config import IMOVEIS_SC_CIDADE, IMOVEIS_SC_MAX_PAGINAS, IMOVEIS_SC_TIPO_NEGOCIO


class CaptadorImoveisSC(CaptadorBase):

    DOMINIO = "https://www.imoveis-sc.com.br"

    def __init__(self, cidade=None, tipo_negocio=None, max_paginas=None):

        self.cidade = (cidade or IMOVEIS_SC_CIDADE).strip().lower()
        self.tipo_negocio = (tipo_negocio or IMOVEIS_SC_TIPO_NEGOCIO).strip().lower()
        self.max_paginas = int(max_paginas or IMOVEIS_SC_MAX_PAGINAS)

        super().__init__(
            nome="IMOVEIS_SC",
            url=f"{self.DOMINIO}/{self.cidade}/{self.tipo_negocio}"
        )

    def capturar(self):

        resultados = []
        vistos_links = set()
        ids_pagina_anterior = None

        for pagina in range(1, self.max_paginas + 1):
            url = self._montar_url_pagina(pagina)
            html = self._baixar_html(url)
            imoveis = self._extrair_imoveis_html(html)
            ids_pagina = [dados.get("id") for dados in imoveis if dados.get("id")]

            if not ids_pagina:
                break

            if ids_pagina_anterior == ids_pagina:
                print(f"IMOVEIS_SC: pagina {pagina} repetida, encerrando paginação.")
                break

            novos_na_pagina = 0
            for dados in imoveis:
                link = self._montar_link(dados)
                if not link or link in vistos_links:
                    continue

                vistos_links.add(link)
                novos_na_pagina += 1
                resultados.append(
                    {
                        "portal": self.nome,
                        "titulo": dados.get("titulo") or "Sem título",
                        "link": link,
                        "dados_imovel": dados,
                    }
                )

            print(f"IMOVEIS_SC: página {pagina} com {novos_na_pagina} novos anúncios.")

            if novos_na_pagina == 0:
                break

            ids_pagina_anterior = ids_pagina

        print(
            "Links encontrados IMOVEIS_SC:",
            len(resultados),
            f"| cidade={self.cidade} tipo={self.tipo_negocio} paginas={self.max_paginas}"
        )
        return resultados

    def _montar_url_pagina(self, pagina):

        if pagina <= 1:
            return self.url

        return f"{self.url}?page={pagina}"

    def _baixar_html(self, url):

        request = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept-Language": "pt-BR,pt;q=0.9",
            },
        )

        with urlopen(request, timeout=20) as resposta:
            return resposta.read().decode("utf-8", errors="ignore")

    def _extrair_imoveis_html(self, html):
        imoveis = []
        vistos = set()

        padroes = [
            re.compile(
                r'\{\\"id\\":\d+,\\"codigo\\":\\".*?\\"localizacao_aproximada_lng\\":(?:null|-?\d+(?:\.\d+)?)\}',
                re.S,
            ),
            re.compile(
                r'\{"id":\d+,"codigo":".*?"localizacao_aproximada_lng":(?:null|-?\d+(?:\.\d+)?)\}',
                re.S,
            ),
        ]

        blocos = []
        for padrao in padroes:
            blocos.extend(padrao.findall(html))

        for bloco in blocos:
            try:
                dados = json.loads(bloco.replace('\\"', '"').replace("\\/", "/"))
            except json.JSONDecodeError:
                continue

            identificador = dados.get("id")
            if not identificador or identificador in vistos:
                continue

            if not dados.get("slug") or not dados.get("slug_cidade") or not dados.get("slug_tipo_negocio"):
                continue

            vistos.add(identificador)
            imoveis.append(dados)

        return imoveis

    def _montar_link(self, dados):

        slug = (dados.get("slug") or "").strip()
        if not slug:
            return ""

        partes = [
            self.DOMINIO,
            (dados.get("slug_cidade") or "").strip("/"),
            (dados.get("slug_tipo_negocio") or "").strip("/"),
        ]

        slug_tipo = (dados.get("slug_tipo_imovel") or "").strip("/")
        slug_bairro = (dados.get("slug_bairro") or "").strip("/")

        if slug_tipo:
            partes.append(slug_tipo)
        if slug_bairro:
            partes.append(slug_bairro)

        base = "/".join(parte for parte in partes if parte)
        return f"{base}/{slug}.html"