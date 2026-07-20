# CAPTADOR IMÓVEIS V2

## Instalação

1. Crie um ambiente virtual Python.
2. Instale dependências:

```bash
python -m pip install -r requirements.txt
```

## Instalação no PC (Windows)

- Execute `instalar_pc.bat` para preparar o ambiente.
- Execute `iniciar_dashboard.bat` para iniciar o painel.
- Guia completo: `INSTALACAO_PC.md`

## Execução

- `python executar.py` — executa o pipeline principal.
- `python executar_painel.py` — exibe o painel de indicadores.
- `python executar_diario.py` — executa rotina diária.
- `python executar_site.py` — inicia painel web com botão para captura, atualização automática e resumo final.

## Produção

Para executar em modo produção com Gunicorn:

`gunicorn -c gunicorn.conf.py wsgi:application`

## Observabilidade

- Logs estruturados de execução: `logs/execucoes.jsonl`
- Cada execução possui `run_id` e métricas por portal.

## Testes

```bash
pytest -q
```

## Observações

- O projeto usa SQLite no arquivo `dados/imoveis.db`.
- A exportação de oportunidades gera `Oportunidades.xlsx`.
- Se precisar, atualize as configurações em `config.py`.
- O pipeline agora inclui o portal ARLETE.
- Se o ARLETE estiver bloqueado por Cloudflare, use o arquivo `dados/arlete_links.txt` com 1 link de imóvel por linha para fallback de captação.
