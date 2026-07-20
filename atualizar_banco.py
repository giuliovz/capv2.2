from banco.database import conectar


banco = conectar()

cursor = banco.cursor()


try:

    cursor.execute(
        """
        ALTER TABLE imoveis
        ADD COLUMN pontuacao INTEGER DEFAULT 0
        """
    )

    print(
        "Coluna pontuacao criada"
    )


except Exception as erro:

    print(
        "pontuacao:",
        erro
    )



try:

    cursor.execute(
        """
        ALTER TABLE imoveis
        ADD COLUMN classificacao TEXT DEFAULT ''
        """
    )

    print(
        "Coluna classificacao criada"
    )


except Exception as erro:

    print(
        "classificacao:",
        erro
    )



banco.commit()

banco.close()