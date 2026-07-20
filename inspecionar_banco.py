from banco.database import conectar

banco = conectar()
cursor = banco.cursor()

cursor.execute("""
SELECT
    id,
    portal,
    titulo,
    bairro,
    valor,
    quartos,
    pontuacao,
    classificacao
FROM imoveis
LIMIT 10
""")

for linha in cursor.fetchall():
    print(linha)

banco.close()