from datetime import datetime



def gerar_resumo(total):


    data = datetime.now().strftime(

        "%d/%m/%Y %H:%M"

    )


    print(

        "Relatório",

        data

    )


    print(

        "Novas oportunidades:",

        total

    )