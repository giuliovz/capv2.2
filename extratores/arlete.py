import re

from modelos.imovel import Imovel
from extratores.base import ExtratorBase


class ExtratorArlete(ExtratorBase):

    def extrair(self, texto, link):

        imagem_urls = self._extrair_imagens_imogestao(texto)

        valor = 0

        valores = re.findall(r"R\$\s?([\d\.,]+)", texto)
        if valores:
            raw = valores[0].replace(".", "").replace(",", ".")
            try:
                valor = int(float(raw))
            except Exception:
                valor = 0

        quartos = 0
        encontrados = re.findall(
            r"(\d+)\s*(?:quartos?|dormi[tóo]rios?|dorms?)",
            texto.lower()
        )
        if encontrados:
            quartos = int(encontrados[0])

        linhas = [l.strip() for l in texto.split("\n") if l.strip()]
        titulo = ""
        if linhas:
            for linha in linhas:
                base = linha.lower()
                if len(linha) > 20 and "ir para" not in base and "menu" not in base:
                    titulo = linha[:150]
                    break
            if not titulo:
                titulo = linhas[0][:150]

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
        elif "terreno" in t_lower:
            tipo = "Terreno"

        bairro = ""
        cidade = ""

        m = re.search(r"bairro[:\s-]*([A-Za-zÀ-ÿ0-9 \-]+)", texto, re.I)
        if m:
            bairro = m.group(1).strip()

        m = re.search(r"cidade[:\s-]*([A-Za-zÀ-ÿ \-]+)", texto, re.I)
        if m:
            cidade = m.group(1).strip()

        banheiros = 0
        suites = 0
        vagas = 0

        m = re.search(r"(\d+)\s*(?:banhei?ros?|wc)\b", texto.lower())
        if m:
            banheiros = int(m.group(1))

        m = re.search(r"(\d+)\s*(?:su[ií]tes?|suite|su[íi]te)\b", texto.lower())
        if m:
            suites = int(m.group(1))

        m = re.search(r"(\d+)\s*(?:vagas?|vaga)\b", texto.lower())
        if m:
            vagas = int(m.group(1))

        area_priv = 0
        area_total = 0

        m = re.search(r"area\s*privativa[:\s-]*(\d+[\d\.,]*)\s*(?:m2|m²|m)\b", texto, re.I)
        if m:
            area_priv = float(m.group(1).replace(".", "").replace(",", "."))
        else:
            m = re.search(r"(\d+[\d\.,]*)\s*(?:m2|m²|m)\b", texto, re.I)
            if m:
                area_priv = float(m.group(1).replace(".", "").replace(",", "."))

        m = re.search(r"area\s*total[:\s-]*(\d+[\d\.,]*)\s*(?:m2|m²|m)\b", texto, re.I)
        if m:
            area_total = float(m.group(1).replace(".", "").replace(",", "."))

        descricao_base = texto[:500]
        if imagem_urls:
            bloco_imagens = "\n\nImagens (ImoGestao):\n" + "\n".join(imagem_urls)
            descricao_base = (descricao_base + bloco_imagens)[:1000]

        return Imovel(
            portal="ARLETE",
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
            descricao=descricao_base
        )

    def _extrair_imagens_imogestao(self, texto):
        urls = re.findall(r"https?://sistema\.imogestao\.com\.br/fotos/\S+", texto)
        unicos = []
        vistos = set()

        for url in urls:
            limpa = url.strip().rstrip(",.;)")
            if limpa in vistos:
                continue
            vistos.add(limpa)
            unicos.append(limpa)

        return unicos[:8]