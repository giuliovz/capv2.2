import sqlite3

from banco.database import conectar


def buscar_indicadores():
    indicadores = {
        "total": 0,
        "media_valor": 0,
        "excelentes": 0,
        "boas": 0,
        "medias": 0,
        "baixas": 0,
    }

    banco = None

    try:
        banco = conectar()
        cursor = banco.cursor()

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
    except sqlite3.DatabaseError as erro:
        print("Painel: falha ao ler indicadores do banco:", erro)
    finally:
        if banco is not None:
            banco.close()

    return indicadores