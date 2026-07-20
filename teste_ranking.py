from painel.ranking import buscar_top_oportunidades

ranking = buscar_top_oportunidades()

print("\nTOP OPORTUNIDADES\n")

for posicao, item in enumerate(ranking, start=1):

    titulo, bairro, valor, pontos, classe, portal, link = item

    print(f"{posicao}º {titulo}")
    print(f"   Bairro: {bairro}")
    print(f"   Valor: R$ {valor:,.2f}")
    print(f"   Pontos: {pontos}")
    print(f"   Classificação: {classe}")
    print(f"   Portal: {portal}")
    print()