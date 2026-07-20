from captadores.gerenciador import executar_todos

from util.navegador import Navegador

from extratores.imoblu import ExtratorImoblu
from extratores.zelt import ExtratorZelt

from banco.database import (
    criar_tabela,
    salvar_imovel
)



def escolher_extrator(portal):

    if portal == "ZELT":

        return ExtratorZelt()

    return ExtratorImoblu()



def executar_pipeline():

    criar_tabela()


    anuncios = executar_todos()


    print(
        "Anúncios capturados:",
        len(anuncios)
    )


    navegador = Navegador()


    salvos = 0


    try:

        for anuncio in anuncios:

            print(
                "Processando:",
                anuncio["link"]
            )


            try:

                pagina = navegador.abrir(

                    anuncio["link"]

                )


                texto = pagina.inner_text(

                    "body"

                )


            except Exception as erro:

                print(
                    "Falha ao abrir:",
                    anuncio["link"],
                    erro
                )

                continue



            extrator = escolher_extrator(

                anuncio["portal"]

            )


            imovel = extrator.extrair(

                texto,

                anuncio["link"]

            )


            if salvar_imovel(imovel):

                salvos += 1



    finally:

        navegador.fechar()



    print(

        "Novos imóveis salvos:",

        salvos

    )