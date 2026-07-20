import os
import sqlite3
from banco.database import BANCO_SQLITE, criar_tabela, conectar


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
