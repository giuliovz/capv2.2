import re

from banco.database import conectar


def _titulo_generico(titulo):
    base = (titulo or "").strip().lower()
    if not base:
        return True
    return base in {
        "ir para o conteúdo",
        "ir para o conteudo",
        "sem título",
        "sem titulo",
    }


def _titulo_por_link(portal, link):
    link = (link or "").strip()
    if not link:
        return "Sem título"

    if portal == "IMOBLU":
        match = re.search(r"id=(\d+)", link)
        if match:
            return f"Imóvel IMOBLU #{match.group(1)}"
        return "Imóvel IMOBLU"

    if portal == "ZELT":
        parte = link.rstrip("/").split("/")[-1]
        if not parte:
            return "Imóvel ZELT"

        # Ex.: apartamento-blumenau-2-quartos-90-m/AP6358-ZLTA
        codigo = parte.split("/")[-1]
        slug = link.rstrip("/").split("/")[-2] if "/imovel/" in link and len(link.rstrip("/").split("/")) >= 2 else ""
        if slug:
            titulo = slug.replace("-", " ").strip().title()
            return f"{titulo} ({codigo})"
        return f"Imóvel ZELT ({codigo})"

    return "Sem título"


def higienizar_dados_imoveis():
    banco = conectar()
    cursor = banco.cursor()

    cursor.execute(
        """
        SELECT id, portal, titulo, bairro, classificacao, link
        FROM imoveis
        """
    )

    registros = cursor.fetchall()
    atualizados = 0

    for item in registros:
        imovel_id, portal, titulo, bairro, classificacao, link = item

        novo_titulo = (titulo or "").strip()
        novo_bairro = (bairro or "").strip()
        nova_classificacao = (classificacao or "").strip()

        if _titulo_generico(novo_titulo):
            novo_titulo = _titulo_por_link(portal, link)

        if not novo_bairro:
            novo_bairro = "Não informado"

        if not nova_classificacao:
            nova_classificacao = "Baixa"

        if (
            novo_titulo != (titulo or "")
            or novo_bairro != (bairro or "")
            or nova_classificacao != (classificacao or "")
        ):
            cursor.execute(
                """
                UPDATE imoveis
                SET titulo = ?,
                    bairro = ?,
                    classificacao = ?
                WHERE id = ?
                """,
                (novo_titulo, novo_bairro, nova_classificacao, imovel_id),
            )
            atualizados += 1

    banco.commit()
    banco.close()
    return atualizados