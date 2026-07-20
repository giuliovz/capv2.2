from urllib.parse import urljoin

from captadores.base import CaptadorBase
from util.navegador import Navegador



class CaptadorImoblu(CaptadorBase):


    def __init__(self):

        super().__init__(

            nome="Imoblu",

            url="https://imoblu.com.br"

        )



    def capturar(self):


        resultados = []


        navegador = Navegador()


        try:

            pagina = navegador.abrir(

                self.url

            )


            pagina.wait_for_timeout(

                3000

            )


            links = pagina.locator(

                "a"

            )


            total = links.count()


            print(

                "Links encontrados:",

                total

            )


            for i in range(total):


                href = links.nth(i).get_attribute(

                    "href"

                )


                texto = links.nth(i).inner_text().strip()



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