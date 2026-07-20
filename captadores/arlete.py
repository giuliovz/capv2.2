from urllib.parse import urljoin
from pathlib import Path

from captadores.base import CaptadorBase
from util.navegador import Navegador
from config import DADOS_DIR


class CaptadorArlete(CaptadorBase):

    def __init__(self):

        super().__init__(

            nome="ARLETE",

            url="https://arletegaldinocorretora.com.br/imoveis?pretensao=comprar"

        )

    def capturar(self):

        resultados = []
        vistos = set()

        navegador = Navegador()

        try:

            pagina = navegador.abrir(self.url)

            pagina.wait_for_timeout(6000)

            # Alguns cards carregam com scroll/lazy loading.
            for _ in range(4):
                pagina.mouse.wheel(0, 2400)
                pagina.wait_for_timeout(800)

            html = pagina.content().lower()
            if "just a moment" in html or "challenges.cloudflare.com" in html:
                print("ARLETE: bloqueado por Cloudflare na coleta automática.")
                return self._capturar_por_arquivo()

            links = pagina.locator("a")
            total = links.count()

            print("Links encontrados ARLETE:", total)

            for i in range(total):

                elemento = links.nth(i)
                href = elemento.get_attribute("href")
                texto = elemento.inner_text().strip()

                if not href:
                    continue

                url = urljoin(self.url, href)

                if "arletegaldinocorretora.com.br" not in url:
                    continue

                if "/imoveis?" in url:
                    continue

                if "/imovel" not in url:
                    continue

                if url in vistos:
                    continue

                vistos.add(url)

                resultados.append(
                    {
                        "portal": self.nome,
                        "titulo": texto or "Sem título",
                        "link": url,
                    }
                )

            if not resultados:
                print("ARLETE: nenhum link de imóvel encontrado na página, usando fallback por arquivo.")
                return self._capturar_por_arquivo()

        finally:

            navegador.fechar()

        return resultados

    def _capturar_por_arquivo(self):

        caminho = DADOS_DIR / "arlete_links.txt"

        if not Path(caminho).exists():
            print("ARLETE: arquivo de fallback não encontrado em dados/arlete_links.txt")
            return []

        linhas = Path(caminho).read_text(encoding="utf-8").splitlines()
        links_validos, relatorio = self._validar_links_fallback(linhas)

        self._salvar_links_limpos(caminho, links_validos)
        self._imprimir_relatorio_validacao(relatorio)

        resultados = [
            {
                "portal": self.nome,
                "titulo": "Sem título",
                "link": link,
            }
            for link in links_validos
        ]

        print("Links carregados por fallback ARLETE:", len(resultados))
        return resultados

    def _validar_links_fallback(self, linhas):

        links_validos = []
        vistos = set()

        relatorio = {
            "lidas": 0,
            "comentarios_ou_vazias": 0,
            "aceitos": 0,
            "rejeitados": 0,
            "rejeitados_formato": 0,
            "rejeitados_dominio": 0,
            "rejeitados_rota": 0,
            "rejeitados_duplicado": 0,
        }

        for linha in linhas:
            relatorio["lidas"] += 1
            link = linha.strip()

            if not link or link.startswith("#"):
                relatorio["comentarios_ou_vazias"] += 1
                continue

            if not link.startswith(("http://", "https://")):
                relatorio["rejeitados"] += 1
                relatorio["rejeitados_formato"] += 1
                continue

            if "arletegaldinocorretora.com.br" not in link:
                relatorio["rejeitados"] += 1
                relatorio["rejeitados_dominio"] += 1
                continue

            if "/imovel" not in link:
                relatorio["rejeitados"] += 1
                relatorio["rejeitados_rota"] += 1
                continue

            if link in vistos:
                relatorio["rejeitados"] += 1
                relatorio["rejeitados_duplicado"] += 1
                continue

            vistos.add(link)
            links_validos.append(link)
            relatorio["aceitos"] += 1

        return links_validos, relatorio

    def _salvar_links_limpos(self, caminho, links_validos):

        cabecalho = [
            "# Fallback de links do portal ARLETE",
            "# Este arquivo foi limpo automaticamente: apenas links válidos e únicos foram mantidos.",
            "# 1 link por linha.",
            "",
        ]
        conteudo = "\n".join(cabecalho + links_validos)
        Path(caminho).write_text(conteudo + "\n", encoding="utf-8")

    def _imprimir_relatorio_validacao(self, relatorio):

        print("ARLETE fallback | relatório de validação:")
        print("- linhas lidas:", relatorio["lidas"])
        print("- comentários/vazias:", relatorio["comentarios_ou_vazias"])
        print("- aceitos:", relatorio["aceitos"])
        print("- rejeitados:", relatorio["rejeitados"])
        print("  - formato inválido:", relatorio["rejeitados_formato"])
        print("  - domínio inválido:", relatorio["rejeitados_dominio"])
        print("  - rota inválida (sem /imovel):", relatorio["rejeitados_rota"])
        print("  - duplicados:", relatorio["rejeitados_duplicado"])