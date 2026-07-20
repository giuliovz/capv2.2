def imovel_interessante(imovel):


    # Tipo permitido

    tipos = [

        "casa",

        "apartamento"

    ]


    tipo = (

        imovel.tipo or ""

    ).lower()



    if tipo:

        if tipo not in tipos:

            return False



    # Quartos mínimos

    if (

        imovel.quartos

        and

        imovel.quartos < 2

    ):

        return False



    # Valor máximo

    limite = 800000


    if (

        imovel.valor

        and

        imovel.valor > limite

    ):

        return False



    return True