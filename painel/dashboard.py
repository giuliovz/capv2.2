from painel.indicadores import buscar_indicadores



def mostrar_dashboard():

    dados = buscar_indicadores()


    print()

    print("=" * 45)

    print("      CAPTADOR IMÓVEIS - PAINEL")

    print("=" * 45)


    print()


    print(
        "Imóveis cadastrados:",
        dados["total"]
    )


    print(
        "Valor médio:",
        f"R$ {dados['media_valor']:,.2f}"
    )


    print()


    print(
        "Oportunidades excelentes:",
        dados["excelentes"]
    )


    print(
        "Boas oportunidades:",
        dados["boas"]
    )


    print()

    print("=" * 45)