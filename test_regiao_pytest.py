from analise.regiao import analisar_regiao, analisar_regiao_detalhada


def test_analisar_regiao_centro_retorna_texto_de_mercado():
    texto = analisar_regiao("Centro", valor=780000, tipo="Apartamento")
    dados = analisar_regiao_detalhada("Centro", valor=780000, tipo="Apartamento")

    assert "Bairro: Centro" in texto
    assert "Mercado" in texto or "mercado" in texto
    assert "faixa intermediária" in texto
    assert dados["tendencia"] in {"alta", "estável", "oportunidade"}
    assert dados["risco_comercial"] in {"baixo", "médio", "alto"}
    assert dados["recomendacao"] in {"abordar agora", "monitorar", "aguardar ajuste de preço"}


def test_analisar_regiao_fallback_para_bairro_desconhecido():
    texto = analisar_regiao("", valor=0, tipo="")
    dados = analisar_regiao_detalhada("", valor=0, tipo="")

    assert "Não informado" in texto
    assert "faixa não informada" in texto
    assert dados["risco_comercial"] in {"baixo", "médio", "alto"}
