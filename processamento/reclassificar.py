from banco.database import conectar

from filtros.pontuacao import (
    calcular_pontuacao,
    classificar
)



def reclassificar_imoveis():


    banco = conectar()

    cursor = banco.cursor()



    cursor.execute(
        """
        SELECT *
        FROM imoveis
        """
    )


    registros = cursor.fetchall()



    total = 0



    for item in registros:


        dados = {

            "tipo": item[3],

            "valor": item[6],

            "quartos": item[7],

            "bairro": item[5],

            "descricao": item[10]

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