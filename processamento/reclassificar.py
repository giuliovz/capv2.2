from banco.database import conectar
from processamento.higienizacao import higienizar_dados_imoveis

from filtros.pontuacao import (
    calcular_pontuacao,
    classificar
)



def reclassificar_imoveis():

    atualizados = higienizar_dados_imoveis()
    if atualizados:
        print("Registros higienizados:", atualizados)


    banco = conectar()

    cursor = banco.cursor()



    cursor.execute(
        """
        SELECT id, tipo, valor, quartos, bairro, descricao
        FROM imoveis
        """
    )


    registros = cursor.fetchall()



    total = 0



    for item in registros:


        dados = {

            "tipo": item[1],

            "valor": item[2],

            "quartos": item[3],

            "bairro": item[4],

            "descricao": item[5]

        }



        pontos = calcular_pontuacao(

            type(
                "Imovel",
                (),
                dados
            )

        )


        nivel = classificar(

            pontos

        )



        cursor.execute(
            """
            UPDATE imoveis

            SET pontuacao = ?,

            classificacao = ?

            WHERE id = ?

            """,

            (

                pontos,

                nivel,

                item[0]

            )

        )


        total += 1



    banco.commit()

    banco.close()



    print(

        "Imóveis reclassificados:",

        total

    )