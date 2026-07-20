import sqlite3

from banco.database import conectar


def buscar_top_oportunidades(limite=10):
    banco = None

    try:
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

        return cursor.fetchall()
    except sqlite3.DatabaseError as erro:
        print("Painel: falha ao ler ranking do banco:", erro)
        return []
    finally:
        if banco is not None:
            banco.close()


def buscar_todos_imoveis():
    banco = None

    try:
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

        return cursor.fetchall()
    except sqlite3.DatabaseError as erro:
        print("Painel: falha ao listar imóveis do banco:", erro)
        return []
    finally:
        if banco is not None:
            banco.close()