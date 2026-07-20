from pathlib import Path

from banco.database import conectar
from painel.indicadores import buscar_indicadores


def _status_banco():
    try:
        banco = conectar()
        cursor = banco.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='imoveis'")
        existe_tabela = cursor.fetchone() is not None
        banco.close()
        return "OK" if existe_tabela else "SEM TABELA"
    except Exception:
        return "ERRO"


def montar_resumo_dashboard(indicadores=None):
    dados = indicadores or buscar_indicadores()
    status_banco = _status_banco()

    linhas = []
    linhas.append("")
    linhas.append("=" * 45)
    linhas.append("      CAPTADOR IMÓVEIS - PAINEL")
    linhas.append("=" * 45)
    linhas.append("")
    linhas.append(f"Status: {status_banco}")
    linhas.append(f"Banco: {Path('dados/imoveis.db').resolve()}")
    linhas.append("")
    linhas.append(f"Imóveis cadastrados: {dados['total']}")
    linhas.append(f"Valor médio: R$ {dados['media_valor']:,.2f}")
    linhas.append("")
    linhas.append(f"Oportunidades excelentes: {dados['excelentes']}")
    linhas.append(f"Boas oportunidades: {dados['boas']}")
    linhas.append(f"Médias: {dados.get('medias', 0)}")
    linhas.append(f"Baixas: {dados.get('baixas', 0)}")
    linhas.append("")
    linhas.append("=" * 45)
    return linhas


def mostrar_dashboard():
    for linha in montar_resumo_dashboard():
        print(linha)