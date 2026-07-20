from filtros.pontuacao import (
    calcular_pontuacao,
    classificar
)



class Imovel:

    tipo = "Apartamento"

    quartos = 3

    valor = 450000

    bairro = "Centro"

    descricao = "Apartamento amplo com ótima localização"



imovel = Imovel()



pontos = calcular_pontuacao(

    imovel

)


print(

    pontos

)


print(

    classificar(pontos)

)