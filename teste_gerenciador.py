from captadores.gerenciador import executar_todos



resultado = executar_todos()



print()

print(

    "TOTAL GERAL:",

    len(resultado)

)


for item in resultado[:10]:

    print(item)