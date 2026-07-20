def calcular_pontuacao(imovel):

    pontos = 0


    tipo = (
        imovel.tipo or ""
    ).lower()


    if tipo in [
        "casa",
        "apartamento"
    ]:

        pontos += 30



    if (
        imovel.quartos
        and imovel.quartos >= 3
    ):

        pontos += 20



    if (
        imovel.valor
        and imovel.valor <= 500000
    ):

        pontos += 20



    descricao = (
        imovel.descricao or ""
    )


    if len(descricao) > 100:

        pontos += 15



    bairros = [

        "centro",
        "velha",
        "vila nova",
        "jardim blumenau"

    ]


    bairro = (

        imovel.bairro or ""

    ).lower()



    for b in bairros:

        if b in bairro:

            pontos += 15

            break



    return pontos




def classificar(pontos):


    if pontos >= 80:

        return "Excelente"


    elif pontos >= 60:

        return "Boa"


    elif pontos >= 40:

        return "Média"


    else:

        return "Baixa"