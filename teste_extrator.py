from extratores.zelt import ExtratorZelt


texto = """
Apartamento Blumenau
3 quartos
R$ 450.000
120 m²
"""


extrator = ExtratorZelt()


imovel = extrator.extrair(

    texto,

    "https://teste.com"

)


print(

    imovel

)


print(

    imovel.para_dict()

)