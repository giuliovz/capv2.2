from util.navegador import Navegador


navegador = Navegador()


pagina = navegador.abrir(

    "https://www.google.com"

)


print(

    "Título:",

    pagina.title()

)


navegador.fechar()