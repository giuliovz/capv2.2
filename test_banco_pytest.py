import os
import sqlite3
from banco.database import BANCO_SQLITE, criar_tabela, conectar
from modelos.imovel import Imovel
from banco.database import salvar_imovel


def test_criar_tabela_and_listar_imoveis(tmp_path, monkeypatch):
    db_path = tmp_path / "imoveis.db"
    monkeypatch.setattr('banco.database.BANCO_SQLITE', db_path)

    criar_tabela()

    banco = conectar()
    cursor = banco.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='imoveis'")

    resultado = cursor.fetchone()
    banco.close()

    assert resultado is not None


def test_criar_tabela_cria_pasta_pai(tmp_path, monkeypatch):
    db_path = tmp_path / "pastas" / "novas" / "imoveis.db"
    monkeypatch.setattr('banco.database.BANCO_SQLITE', db_path)

    criar_tabela()

    assert db_path.exists()
    assert db_path.parent.exists()


def test_salvar_imovel_persiste_pontuacao_e_classificacao(tmp_path, monkeypatch):
    db_path = tmp_path / "imoveis.db"
    monkeypatch.setattr('banco.database.BANCO_SQLITE', db_path)

    criar_tabela()

    imovel = Imovel(
        portal="IMOVEIS_SC",
        link="https://example.com/imovel-1",
        codigo="ABC123",
        titulo="Apartamento teste",
        bairro="Centro",
        cidade="Blumenau",
        valor=500000,
        quartos=2,
        pontuacao=88,
        classificacao="Excelente",
    )

    assert salvar_imovel(imovel) is True

    banco = conectar()
    cursor = banco.cursor()
    cursor.execute(
        "SELECT portal, link, pontuacao, classificacao FROM imoveis WHERE link = ?",
        (imovel.link,)
    )
    resultado = cursor.fetchone()
    banco.close()

    assert resultado == ("IMOVEIS_SC", "https://example.com/imovel-1", 88, "Excelente")
