from filtros.comercial import imovel_interessante



class Teste:

    tipo = "Apartamento"

    quartos = 3

    valor = 450000



imovel = Teste()



resultado = imovel_interessante(

    imovel

)



print(resultado)