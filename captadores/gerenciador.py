from captadores.imoblu import CaptadorImoblu
from captadores.zelt import CaptadorZelt



def executar_todos():


    todos = []


    captadores = [

        CaptadorImoblu(),

        CaptadorZelt()

    ]



    for captador in captadores:


        print()

        print(

            "Executando:",

            captador.nome

        )


        try:


            resultado = captador.capturar()


            print(

                "Encontrados:",

                len(resultado)

            )


            todos.extend(

                resultado

            )


        except Exception as erro:


            print(

                "Erro no captador:",

                captador.nome,

                erro

            )



    return remover_duplicados(

        todos

    )




def remover_duplicados(lista):


    vistos = set()

    resultado = []



    for item in lista:


        link = item.get(

            "link"

        )



        if link not in vistos:


            vistos.add(link)

            resultado.append(item)



    return resultado