from banco.database import conectar


def buscar_top_oportunidades(limite=10):

    banco = conectar()
    cursor = banco.cursor()

    cursor.execute(
        """
        SELECT
            titulo,
            bairro,
            valor,
            pontuacao,
            classificacao,
            portal,
            link
        FROM imoveis
        ORDER BY pontuacao DESC, valor ASC
        LIMIT ?
        """,
        (limite,)
    )

    resultados = cursor.fetchall()

    banco.close()

    return resultados


def buscar_todos_imoveis():

    banco = conectar()
    cursor = banco.cursor()

    cursor.execute(
        """
        SELECT
            titulo,
            bairro,
            valor,
            pontuacao,
            classificacao,
            portal,
            link
        FROM imoveis
        ORDER BY pontuacao DESC, valor ASC
        """
    )

    resultados = cursor.fetchall()

    banco.close()

    return resultados