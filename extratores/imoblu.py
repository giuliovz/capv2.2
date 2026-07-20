import re

from modelos.imovel import Imovel
from extratores.base import ExtratorBase


class ExtratorImoblu(ExtratorBase):

    def extrair(self, texto, link):

        valor = 0

        valores = re.findall(
            r"R\$\s?([\d\.,]+)",
            texto
        )

        if valores:
            raw = valores[0]
            raw = raw.replace('.', '').replace(',', '.')
            try:
                valor = int(float(raw))
            except Exception:
                try:
                    valor = int(raw)
                except Exception:
                    valor = 0

        quartos = 0

        # quartos / dormitórios (aceitar variações: quarto, quartos, dorm, dormitórios)
        encontrados = re.findall(
            r"(\d+)\s*(?:quartos?|dormi[tóo]rios?|dorms?)",
            texto.lower()
        )

        if encontrados:
            quartos = int(encontrados[0])

        titulo = ""
        linhas = [l.strip() for l in texto.split("\n") if l.strip()]

        if linhas:
            # escolha a primeira linha significativa (ignorar links de skip ou curtas)
            titulo = ""
            for l in linhas:
                if len(l) > 20 and 'ir para' not in l.lower() and 'pular' not in l.lower():
                    titulo = l[:150]
                    break
            if not titulo:
                titulo = linhas[0][:150]

        # tipo
        tipo = ""
        t_lower = texto.lower()
        if "apartamento" in t_lower:
            tipo = "Apartamento"
        elif "cobertura" in t_lower:
            tipo = "Cobertura"
        elif "casa" in t_lower:
            tipo = "Casa"
        elif "sala" in t_lower:
            tipo = "Sala"

        # bairro e cidade (heurísticas)
        bairro = ""
        cidade = ""

        m = re.search(r"bairro[:\s-]*([A-Za-zÀ-ÿ0-9 \-]+)", texto, re.I)
        if m:
            bairro = m.group(1).strip()

        m = re.search(r"cidade[:\s-]*([A-Za-zÀ-ÿ \-]+)", texto, re.I)
        if m:
            cidade = m.group(1).strip()

        # banheiros, suites, vagas
        banheiros = 0
        suites = 0
        vagas = 0

        # banheiros, suites, vagas (variações e proximidade)
        m = re.search(r"(\d+)\s*(?:banhei?ros?|banheiro|banheiros|wc)\b", texto.lower())
        if m:
            banheiros = int(m.group(1))

        m = re.search(r"(\d+)\s*(?:su[ií]tes?|suite|su[íi]te)\b", texto.lower())
        if m:
            suites = int(m.group(1))

        m = re.search(r"(\d+)\s*(?:vagas?|vaga)\b", texto.lower())
        if m:
            vagas = int(m.group(1))

        # áreas (m2)
        area_priv = 0
        area_total = 0

        # áreas (privativa / total) - aceitar variações e separadores
        m = re.search(r"area\s*privativa[:\s-]*(\d+[\d\.,]*)\s*(?:m2|m²|m)\b", texto, re.I)
        if m:
            area_priv = float(m.group(1).replace('.', '').replace(',', '.'))
        else:
            # fallback: primeiro valor em m2
            m = re.search(r"(\d+[\d\.,]*)\s*(?:m2|m²|m)\b", texto, re.I)
            if m:
                area_priv = float(m.group(1).replace('.', '').replace(',', '.'))

        m = re.search(r"area\s*total[:\s-]*(\d+[\d\.,]*)\s*(?:m2|m²|m)\b", texto, re.I)
        if m:
            area_total = float(m.group(1).replace('.', '').replace(',', '.'))

        return Imovel(
            portal="IMOBLU",
            link=link,
            titulo=titulo,
            tipo=tipo,
            bairro=bairro,
            cidade=cidade,
            valor=valor,
            quartos=quartos,
            suites=suites,
            banheiros=banheiros,
            vagas=vagas,
            area_privativa=area_priv,
            area_total=area_total,
            descricao=texto[:500]
        )