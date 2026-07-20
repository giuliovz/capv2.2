from dataclasses import dataclass


@dataclass
class ResultadoQualidade:
    score: int
    motivos: list[str]
    bloquear: bool


def avaliar_imovel(imovel) -> ResultadoQualidade:
    motivos = []
    score = 100

    titulo = (imovel.titulo or "").strip()
    bairro = (imovel.bairro or "").strip()
    valor = float(imovel.valor or 0)
    quartos = int(imovel.quartos or 0)
    descricao = (imovel.descricao or "").strip()

    if not titulo or titulo.lower() in {"ir para o conteúdo", "ir para o conteudo", "sem título", "sem titulo"}:
        motivos.append("titulo_fraco")
        score -= 25

    if not bairro:
        motivos.append("bairro_ausente")
        score -= 20

    if valor <= 0:
        motivos.append("valor_ausente")
        score -= 30

    if quartos <= 0:
        motivos.append("quartos_ausentes")
        score -= 10

    if len(descricao) < 80:
        motivos.append("descricao_curta")
        score -= 10

    score = max(0, min(100, score))

    # Bloqueio para registros com baixa confianca e sem dados basicos.
    bloquear = score < 35 and (valor <= 0 or not bairro)

    return ResultadoQualidade(score=score, motivos=motivos, bloquear=bloquear)
