import sqlite3
from pathlib import Path

from config import BANCO_SQLITE


def conectar():
    caminho = Path(BANCO_SQLITE)
    caminho.parent.mkdir(exist_ok=True, parents=True)

    return sqlite3.connect(caminho)


def criar_tabela():

    banco = conectar()

    cursor = banco.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS imoveis (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            portal TEXT,

            codigo TEXT,

            tipo TEXT,

            finalidade TEXT,

            titulo TEXT,

            bairro TEXT,

            cidade TEXT,

            valor REAL,

            quartos INTEGER,

            suites INTEGER,

            banheiros INTEGER,

            vagas INTEGER,

            area_privativa REAL,

            area_total REAL,

            descricao TEXT,

            link TEXT UNIQUE,

            data_captura TEXT,

            status TEXT,

            pontuacao INTEGER DEFAULT 0,

    classificacao TEXT DEFAULT ''

        )
        """
    )


    banco.commit()

    banco.close()



def existe_imovel(link):

    banco = conectar()

    cursor = banco.cursor()


    cursor.execute(
        """
        SELECT id 
        FROM imoveis
        WHERE link = ?
        """,
        (link,)
    )


    resultado = cursor.fetchone()


    banco.close()


    return resultado is not None



def salvar_imovel(imovel):

    if existe_imovel(
        imovel.link
    ):

        return False


    banco = conectar()

    cursor = banco.cursor()


    dados = imovel.para_dict()


    cursor.execute(
        """
        INSERT INTO imoveis (

            portal,
            codigo,
            tipo,
            finalidade,
            titulo,
            bairro,
            cidade,
            valor,
            quartos,
            suites,
            banheiros,
            vagas,
            area_privativa,
            area_total,
            descricao,
            link,
            data_captura,
            status

        )

        VALUES (

            :portal,
            :codigo,
            :tipo,
            :finalidade,
            :titulo,
            :bairro,
            :cidade,
            :valor,
            :quartos,
            :suites,
            :banheiros,
            :vagas,
            :area_privativa,
            :area_total,
            :descricao,
            :link,
            :data_captura,
            :status

        )
        """,
        dados
    )


    banco.commit()

    banco.close()


    return True



def listar_imoveis():

    banco = conectar()

    cursor = banco.cursor()


    cursor.execute(
        """
        SELECT *
        FROM imoveis
        """
    )


    dados = cursor.fetchall()


    banco.close()


    return dados