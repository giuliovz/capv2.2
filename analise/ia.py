import re
from typing import Tuple


def analisar_imovel(imovel) -> Tuple[int, str]:
    """Análise leve de oportunidade baseada em regras e texto do anúncio."""
    texto = (imovel.descricao or "").lower()
    tipo = (imovel.tipo or "").lower()
    bairro = (imovel.bairro or "").lower()
    valor = float(imovel.valor or 0)
    quartos = int(imovel.quartos or 0)

    pontos = 0

    if tipo in {"casa", "apartamento"}:
        pontos += 25

    if quartos >= 3:
        pontos += 20
    elif quartos == 2:
        pontos += 10

    if valor and valor <= 700000:
        pontos += 20
    elif valor and valor <= 1000000:
        pontos += 10

    if len(texto) > 120:
        pontos += 10

    if any(token in bairro for token in ["centro", "velha", "vila nova", "jardim", "blumenau"]):
        pontos += 15

    if any(token in texto for token in ["otimo", "excelente", "muito", "novo", "bem localizado", "vista", "piso"]):
        pontos += 10

    if any(token in texto for token in ["condominio", "mobilia", "garagem", "piscina", "academia", "churrasqueira"]):
        pontos += 5

    if re.search(r"\b(garagem|vaga|vagas)\b", texto):
        pontos += 5

    if pontos >= 80:
        classificacao = "Excelente"
    elif pontos >= 60:
        classificacao = "Boa"
    elif pontos >= 40:
        classificacao = "Média"
    else:
        classificacao = "Baixa"

    return pontos, classificacao


def opinar_top_imovel(titulo, bairro, valor, pontuacao, classificacao, portal, tom="equilibrado"):
    titulo = (titulo or "Sem título").strip()
    bairro = (bairro or "Não informado").strip()
    portal = (portal or "-" ).strip()
    valor = float(valor or 0)
    pontuacao = int(pontuacao or 0)
    classificacao = (classificacao or "Baixa").strip()

    pontos_fortes = []
    alertas = []

    if pontuacao >= 80:
        pontos_fortes.append("pontuação muito alta")
    elif pontuacao >= 60:
        pontos_fortes.append("pontuação consistente")
    else:
        alertas.append("pontuação abaixo do ideal para prioridade")

    if classificacao == "Excelente":
        pontos_fortes.append("classificação excelente")
    elif classificacao == "Boa":
        pontos_fortes.append("classificação boa")
    elif classificacao == "Média":
        alertas.append("classificação média")
    else:
        alertas.append("classificação baixa")

    if bairro and bairro.lower() != "não informado":
        pontos_fortes.append(f"localização em {bairro}")
    else:
        alertas.append("bairro sem detalhamento")

    if valor <= 0:
        alertas.append("valor indisponível")
    elif valor <= 700000:
        pontos_fortes.append("faixa de valor potencialmente atrativa")
    elif valor >= 1800000:
        alertas.append("ticket elevado, público mais restrito")

    resumo = f"{titulo} ({portal})"

    tom = (tom or "equilibrado").strip().lower()

    if tom == "conservador":
        if not pontos_fortes:
            opiniao = "Recomendação conservadora: manter em monitoramento até validações complementares."
        elif classificacao in {"Excelente", "Boa"} and pontuacao >= 75:
            opiniao = "Recomendação conservadora: avançar contato com cautela, priorizando confirmação documental e liquidez."
        else:
            opiniao = "Recomendação conservadora: abordagem seletiva e validação detalhada antes de priorizar."
    elif tom == "agressivo":
        if not pontos_fortes:
            opiniao = "Recomendação agressiva: testar abordagem rápida para medir tração, mesmo com sinais moderados."
        elif classificacao in {"Excelente", "Boa"} and pontuacao >= 60:
            opiniao = "Recomendação agressiva: prioridade alta de contato e proposta comercial imediata."
        else:
            opiniao = "Recomendação agressiva: manter no funil ativo e acelerar qualificação comercial."
    else:
        if not pontos_fortes:
            opiniao = "Recomendação de monitoramento, sem gatilho forte de prioridade imediata."
        elif classificacao in {"Excelente", "Boa"} and pontuacao >= 60:
            opiniao = "Recomendação de abordagem comercial prioritária para contato e proposta."
        else:
            opiniao = "Recomendação de abordagem seletiva, com validação adicional antes do contato."

    trecho_forte = ", ".join(pontos_fortes[:3]) if pontos_fortes else "sem diferenciais claros"
    trecho_alerta = "; alerta: " + ", ".join(alertas[:3]) if alertas else ""

    return f"{resumo}: {opiniao} Base da análise: {trecho_forte}{trecho_alerta}."
