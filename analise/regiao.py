def _normalizar(texto):
    return (texto or "").strip().lower()


def analisar_regiao_detalhada(bairro, valor=0, tipo=""):
    bairro_raw = (bairro or "Não informado").strip()
    bairro_key = _normalizar(bairro)
    tipo_key = _normalizar(tipo)
    valor = float(valor or 0)

    descricao_regiao = "Região com perfil misto, variando entre uso residencial e comercial."
    mercado = "Mercado com liquidez moderada e forte dependência de preço competitivo."
    tendencia = "estável"
    risco_comercial = "médio"
    recomendacao = "monitorar"

    if any(k in bairro_key for k in ["centro", "jardim blumenau", "victor konder"]):
        descricao_regiao = "Região central com alta oferta de serviços, mobilidade e procura constante."
        mercado = "Mercado aquecido para locação e venda, com ticket médio acima da cidade em imóveis bem localizados."
        tendencia = "alta"
        risco_comercial = "baixo"
        recomendacao = "abordar agora"
    elif any(k in bairro_key for k in ["velha", "escola agrícola", "vila nova"]):
        descricao_regiao = "Região residencial consolidada, com boa infraestrutura urbana e acesso rápido aos principais eixos."
        mercado = "Mercado estável, boa absorção para famílias e investidores que buscam equilíbrio entre preço e localização."
        tendencia = "estável"
        risco_comercial = "médio"
        recomendacao = "monitorar"
    elif any(k in bairro_key for k in ["itoupava", "salto", "fortaleza", "garcia"]):
        descricao_regiao = "Região em expansão com bairros de perfil familiar e desenvolvimento contínuo."
        mercado = "Mercado com potencial de valorização no médio prazo, especialmente em imóveis com boa metragem e padrão construtivo."
        tendencia = "oportunidade"
        risco_comercial = "médio"
        recomendacao = "abordar agora"
    elif any(k in bairro_key for k in ["ponta aguda", "agua verde", "água verde"]):
        descricao_regiao = "Região com combinação de áreas residenciais e pontos de interesse comerciais."
        mercado = "Mercado dinâmico para locação, com sensibilidade ao preço e à qualidade do acabamento."
        tendencia = "estável"
        risco_comercial = "médio"
        recomendacao = "monitorar"

    faixa = "faixa não informada"
    if valor > 0:
        if valor < 500000:
            faixa = "faixa de entrada"
            if recomendacao != "abordar agora":
                recomendacao = "abordar agora"
        elif valor < 1000000:
            faixa = "faixa intermediária"
        else:
            faixa = "faixa premium"
            risco_comercial = "alto"
            recomendacao = "aguardar ajuste de preço"

    perfil_tipo = "imóvel"
    if "apart" in tipo_key:
        perfil_tipo = "apartamento"
    elif "casa" in tipo_key:
        perfil_tipo = "casa"
    elif "sala" in tipo_key:
        perfil_tipo = "sala comercial"
    elif "cobertura" in tipo_key:
        perfil_tipo = "cobertura"

    resumo = (
        f"Bairro: {bairro_raw}. "
        f"{descricao_regiao} "
        f"Para {perfil_tipo} na {faixa}, {mercado}"
    )

    return {
        "bairro": bairro_raw,
        "resumo": resumo,
        "tendencia": tendencia,
        "risco_comercial": risco_comercial,
        "recomendacao": recomendacao,
    }


def analisar_regiao(bairro, valor=0, tipo=""):
    dados = analisar_regiao_detalhada(bairro=bairro, valor=valor, tipo=tipo)
    return dados["resumo"]