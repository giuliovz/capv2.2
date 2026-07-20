from config import (
    DADOS_DIR,
    RELATORIOS_DIR,
    LOGS_DIR
)


def preparar_pastas():
    for pasta in (DADOS_DIR, RELATORIOS_DIR, LOGS_DIR):
        pasta.mkdir(exist_ok=True, parents=True)


def main():
    preparar_pastas()

    print("=" * 40)
    print("CAPTADOR IMÓVEIS V2")
    print("=" * 40)
    print("Projeto iniciado com sucesso.")
    print("Próximo módulo: Banco de Dados.")


if __name__ == "__main__":
    main()