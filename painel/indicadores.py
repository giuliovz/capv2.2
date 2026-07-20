from banco.database import conectar


def buscar_indicadores():


    banco = conectar()

    cursor = banco.cursor()



    indicadores = {}



    cursor.execute(
        """
        SELECT COUNT(*)
        FROM imoveis
        """
    )

    indicadores["total"] = cursor.fetchone()[0]



    cursor.execute(
        """
        SELECT AVG(valor)
        FROM imoveis
        WHERE valor > 0
        """
    )

    media = cursor.fetchone()[0]


    indicadores["media_valor"] = media or 0



    cursor.execute(
        """
        SELECT COUNT(*)
        FROM imoveis
        WHERE classificacao = 'Excelente'
        """
    )

    indicadores["excelentes"] = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM imoveis
        WHERE classificacao = 'Boa'
        """
    )

    indicadores["boas"] = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM imoveis
        WHERE classificacao = 'Média'
        """
    )

    indicadores["medias"] = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM imoveis
        WHERE classificacao = 'Baixa'
        """
    )

    indicadores["baixas"] = cursor.fetchone()[0]



    banco.close()


    return indicadores