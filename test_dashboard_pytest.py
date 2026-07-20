from painel.dashboard import montar_resumo_dashboard


def test_montar_resumo_dashboard_inclui_status_e_indicadores():
    linhas = montar_resumo_dashboard(
        indicadores={
            "total": 7,
            "media_valor": 150000.0,
            "excelentes": 2,
            "boas": 3,
        }
    )

    texto = "\n".join(linhas)

    assert "CAPTADOR IMÓVEIS - PAINEL" in texto
    assert "Status:" in texto
    assert "Banco:" in texto
    assert "Imóveis cadastrados: 7" in texto
    assert "Valor médio: R$ 150,000.00" in texto
