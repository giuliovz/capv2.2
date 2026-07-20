from urllib.parse import urljoin

from captadores.base import CaptadorBase
from util.navegador import Navegador



class CaptadorZelt(CaptadorBase):


    def __init__(self):

        super().__init__(

            nome="ZELT",

            url="https://www.zelt.com.br/imoveis"

        )



    def capturar(self):


        resultados = []


        navegador = Navegador()


        try:

            pagina = navegador.abrir(

                self.url

            )


            pagina.wait_for_timeout(

                5000

            )


            links = pagina.locator(

                "a"

            )


            total = links.count()


            print(

                "Links encontrados ZELT:",

                total

            )



            for i in range(total):


                elemento = links.nth(i)


                href = elemento.get_attribute(

                    "href"

                )


                texto = elemento.inner_text().strip()



                if not href:

                    continue



                url = urljoin(

                    self.url,

                    href

                )



                if "/imovel/" in url:


                    resultados.append(

                        {

                            "portal": self.nome,

                            "titulo": texto,

                            "link": url

                        }

                    )



        finally:

            navegador.fechar()



        return resultados