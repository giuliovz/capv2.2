from painel.ranking import buscar_top_oportunidades
from banco.database import conectar, criar_tabela


def test_buscar_top_oportunidades_retornando_lista(tmp_path, monkeypatch):
    db_path = tmp_path / "imoveis.db"
    monkeypatch.setattr('banco.database.BANCO_SQLITE', db_path)

    criar_tabela()
    banco = conectar()
    cursor = banco.cursor()
    cursor.execute(
        "INSERT INTO imoveis (titulo, bairro, valor, pontuacao, classificacao, portal, link) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("Imóvel 1", "Centro", 300000, 80, "Excelente", "IMOBLU", "link1")
    )
    banco.commit()
    banco.close()

    ranking = buscar_top_oportunidades(limite=1)

    assert len(ranking) == 1
    assert ranking[0][0] == "Imóvel 1"
