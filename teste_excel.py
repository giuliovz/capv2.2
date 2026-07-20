from exportacao.excel import exportar_excel



class Imovel:


    portal="ZELT"

    tipo="Apartamento"

    titulo="Apartamento Centro"

    bairro="Centro"

    cidade="Blumenau"

    valor=450000

    quartos=3

    area_privativa=120

    link="teste"



imovel = Imovel()



exportar_excel(

    [imovel]

)