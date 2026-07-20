from pathlib import Path

# Pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent

# Pastas
DADOS_DIR = BASE_DIR / "dados"
RELATORIOS_DIR = BASE_DIR / "relatorios"
LOGS_DIR = BASE_DIR / "logs"

# Banco de dados
BANCO_SQLITE = DADOS_DIR / "imoveis.db"

# Arquivo Excel
ARQUIVO_EXCEL = RELATORIOS_DIR / "captacao.xlsx"

# Configurações do navegador
HEADLESS = True
TIMEOUT = 60000

# Filtros (você poderá alterar depois)
FINALIDADE = "Venda"

# Configuração do portal Imóveis-SC
IMOVEIS_SC_CIDADE = "blumenau"
IMOVEIS_SC_TIPO_NEGOCIO = "comprar"
IMOVEIS_SC_MAX_PAGINAS = 5

TIPOS_PERMITIDOS = [
    "Casa",
    "Apartamento",
    "Sobrado",
    "Geminado",
    "Cobertura",
    "Terreno",
    "Sala Comercial",
    "Galpão",
    "Chácara",
    "Sítio"
]