from captadores.base import CaptadorBase



class CaptadorTeste(CaptadorBase):


    def capturar(self):

        return [

            {

                "portal": self.nome,

                "link": self.url

            }

        ]



captador = CaptadorTeste(

    "Teste",

    "https://teste.com"

)



print(

    captador.informacao()

)


print(

    captador.capturar()

)