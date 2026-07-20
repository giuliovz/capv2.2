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