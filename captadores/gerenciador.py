from captadores.imoblu import CaptadorImoblu
from captadores.zelt import CaptadorZelt
from captadores.arlete import CaptadorArlete
from captadores.imoveis_sc import CaptadorImoveisSC
import time



def executar_todos():


    todos = []


    captadores = [

        CaptadorImoblu(),

        CaptadorZelt(),

        CaptadorArlete(),

        CaptadorImoveisSC()

    ]



    for captador in captadores:


        print()

        print(

            "Executando:",

            captador.nome

        )


        tentativas = 3
        resultado = []

        for tentativa in range(1, tentativas + 1):
            try:
                resultado = captador.capturar()
                break
            except Exception as erro:
                print("Erro no captador:", captador.nome, erro)
                if tentativa == tentativas:
                    print("Captador sem sucesso apos tentativas:", captador.nome)
                    resultado = []
                else:
                    espera = tentativa * 2
                    print(f"Retry {tentativa}/{tentativas - 1} em {espera}s...")
                    time.sleep(espera)

        print(

            "Encontrados:",

            len(resultado)

        )


        todos.extend(

            resultado

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