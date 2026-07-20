from modelos.imovel import Imovel


imovel = Imovel(

    portal="Teste",

    link="https://teste.com",

    tipo="Casa",

    bairro="Tribess",

    cidade="Blumenau",

    valor=390000,

    quartos=3

)


print(imovel)

print()

print(imovel.para_dict())