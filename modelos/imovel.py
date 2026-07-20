from dataclasses import dataclass


@dataclass
class Imovel:

    portal: str = ""

    link: str = ""

    codigo: str = ""

    titulo: str = ""

    tipo: str = ""

    bairro: str = ""

    cidade: str = ""

    valor: float = 0.0

    quartos: int = 0

    suites: int = 0

    banheiros: int = 0

    vagas: int = 0

    area: float = 0.0

    descricao: str = ""

    pontuacao: int = 0

    classificacao: str = "Baixa"

    def to_dict(self):

        return {
            "portal": self.portal,
            "link": self.link,
            "codigo": self.codigo,
            "titulo": self.titulo,
            "tipo": self.tipo,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "valor": self.valor,
            "quartos": self.quartos,
            "suites": self.suites,
            "banheiros": self.banheiros,
            "vagas": self.vagas,
            "area": self.area,
            "descricao": self.descricao,
            "pontuacao": self.pontuacao,
            "classificacao": self.classificacao,
        }