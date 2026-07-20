from painel.html_dashboard import abrir_dashboard_html, gerar_html_dashboard


if __name__ == "__main__":
    abrir = input("Abrir o dashboard no navegador? [s/N]: ").strip().lower() == "s"
    caminho = gerar_html_dashboard()
    print(f"Dashboard HTML gerado em: {caminho}")
    if abrir:
        abrir_dashboard_html(caminho)
        print("Dashboard aberto no navegador.")
