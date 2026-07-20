from captadores.imoblu import CaptadorImoblu



captador = CaptadorImoblu()



resultado = captador.capturar()



print()

print(

    "Total:",

    len(resultado)

)


for item in resultado[:5]:

    print(item)