from captadores.zelt import CaptadorZelt



captador = CaptadorZelt()


resultado = captador.capturar()


print()

print(

    "Total ZELT:",

    len(resultado)

)


for item in resultado[:5]:

    print(item)