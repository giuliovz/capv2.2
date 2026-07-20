from captadores.gerenciador import executar_todos
from urllib.parse import urljoin
import time
from uuid import uuid4

from util.navegador import Navegador

from extratores.imoblu import ExtratorImoblu
from extratores.zelt import ExtratorZelt
from extratores.arlete import ExtratorArlete

from banco.database import (
    criar_tabela,
    salvar_imovel
)

from exportacao.excel import exportar_excel
from analise.ia import analisar_imovel
from painel.html_dashboard import gerar_html_dashboard
from processamento.higienizacao import higienizar_dados_imoveis
from processamento.observabilidade import ObservabilidadeExecucao
from processamento.qualidade import avaliar_imovel


ETAPAS_PROGRESSO = [
    "captura",
    "extracao",
    "classificacao",
    "exportacao",
    "dashboard",
]


def _emitir_progresso(progress_callback, etapa, percentual, mensagem):
    if not progress_callback:
        return

    etapas = []
    for nome in ETAPAS_PROGRESSO:
        if nome == etapa:
            status = "executando"
        elif ETAPAS_PROGRESSO.index(nome) < ETAPAS_PROGRESSO.index(etapa):
            status = "concluida"
        else:
            status = "pendente"

        etapas.append(
            {
                "nome": nome,
                "status": status,
            }
        )

    progress_callback(
        {
            "etapa": etapa,
            "percentual": max(0, min(100, int(percentual))),
            "mensagem": mensagem,
            "etapas": etapas,
        }
    )


def _titulo_generico(titulo):
    base = (titulo or "").strip().lower()
    return base in {
        "",
        "ir para o conteúdo",
        "ir para o conteudo",
        "sem título",
        "sem titulo",
    }


def _imovel_invalido(imovel):
    titulo_invalido = _titulo_generico(imovel.titulo)
    bairro_vazio = not (imovel.bairro or "").strip()
    sem_valor = float(imovel.valor or 0) <= 0
    sem_quartos = int(imovel.quartos or 0) <= 0

    # Evita salvar páginas de navegação/placeholder sem dados reais do imóvel.
    return titulo_invalido and bairro_vazio and sem_valor and sem_quartos


def _coletar_midias_imogestao(pagina, url_base, limite=8):
    urls = []
    vistos = set()

    try:
        imagens = pagina.locator("img")
        total = imagens.count()

        for i in range(total):
            src = imagens.nth(i).get_attribute("src")
            if not src:
                continue

            src_abs = urljoin(url_base, src)

            if "sistema.imogestao.com.br/fotos/" not in src_abs:
                continue

            if src_abs in vistos:
                continue

            vistos.add(src_abs)
            urls.append(src_abs)

            if len(urls) >= limite:
                break

    except Exception:
        pass

    return urls


def _abrir_com_retry(navegador, link, tentativas=3):
    ultimo_erro = None

    for tentativa in range(1, tentativas + 1):
        try:
            pagina = navegador.abrir(link)
            texto = pagina.inner_text("body")
            if texto and len(texto.strip()) > 0:
                return pagina, texto
        except Exception as erro:
            ultimo_erro = erro

        if tentativa < tentativas:
            time.sleep(tentativa * 1.5)

    if ultimo_erro:
        raise ultimo_erro

    raise RuntimeError("Falha ao carregar conteudo da pagina")



def escolher_extrator(portal):

    if portal == "ZELT":

        return ExtratorZelt()

    if portal == "ARLETE":

        return ExtratorArlete()

    return ExtratorImoblu()



def executar_pipeline(progress_callback=None, tom_ia="equilibrado"):

    run_id = str(uuid4())
    obs = ObservabilidadeExecucao(run_id)
    obs.evento("inicio_execucao", {"tom_ia": tom_ia})

    criar_tabela()
    _emitir_progresso(progress_callback, "captura", 5, "Preparando ambiente e dados...")

    atualizados = higienizar_dados_imoveis()
    obs.evento("higienizacao", {"registros_atualizados": atualizados})
    if atualizados:
        print("Registros higienizados:", atualizados)

    _emitir_progresso(progress_callback, "captura", 15, "Capturando anúncios nos portais...")

    anuncios = executar_todos()
    obs.evento("captura_links", {"total_anuncios": len(anuncios)})


    print(
        "Anúncios capturados:",
        len(anuncios)
    )

    _emitir_progresso(progress_callback, "extracao", 20, "Extraindo dados dos anúncios...")


    navegador = Navegador()


    salvos = 0
    descartados = 0
    falhas_abertura = 0
    processados = 0
    soma_score_qualidade = 0
    total_score_qualidade = 0
    imoveis_capturados = []
    metricas_portal = {}


    try:

        for anuncio in anuncios:
            portal_nome = anuncio.get("portal", "DESCONHECIDO")
            if portal_nome not in metricas_portal:
                metricas_portal[portal_nome] = {
                    "capturados": 0,
                    "processados": 0,
                    "salvos": 0,
                    "descartados": 0,
                    "falhas_abertura": 0,
                }
            metricas_portal[portal_nome]["capturados"] += 1

            if anuncios:
                base = 20
                faixa = 45
                percentual_item = base + int((processados / len(anuncios)) * faixa)
                _emitir_progresso(
                    progress_callback,
                    "extracao",
                    percentual_item,
                    f"Extraindo anúncio {processados + 1} de {len(anuncios)}...",
                )

            print(
                "Processando:",
                anuncio["link"]
            )


            try:
                pagina, texto = _abrir_com_retry(navegador, anuncio["link"], tentativas=3)

                if anuncio["portal"] == "ARLETE":
                    midias = _coletar_midias_imogestao(pagina, anuncio["link"])
                    if midias:
                        texto = (
                            texto
                            + "\n\nIMAGENS_IMOGESTAO:\n"
                            + "\n".join(midias)
                        )


            except Exception as erro:

                print(
                    "Falha ao abrir:",
                    anuncio["link"],
                    erro
                )

                falhas_abertura += 1
                metricas_portal[portal_nome]["falhas_abertura"] += 1
                obs.evento(
                    "falha_abertura",
                    {
                        "portal": portal_nome,
                        "link": anuncio.get("link"),
                        "erro": str(erro),
                    },
                )

                continue



            extrator = escolher_extrator(

                anuncio["portal"]

            )


            imovel = extrator.extrair(

                texto,

                anuncio["link"]

            )

            if anuncios:
                base = 65
                faixa = 15
                percentual_class = base + int((processados / len(anuncios)) * faixa)
                _emitir_progresso(
                    progress_callback,
                    "classificacao",
                    percentual_class,
                    f"Classificando anúncio {processados + 1} de {len(anuncios)}...",
                )

            pontos, classificacao = analisar_imovel(imovel)
            imovel.pontuacao = pontos
            imovel.classificacao = classificacao

            qualidade = avaliar_imovel(imovel)
            soma_score_qualidade += qualidade.score
            total_score_qualidade += 1

            if _imovel_invalido(imovel):
                print("Registro descartado por dados insuficientes:", anuncio["link"])
                descartados += 1
                metricas_portal[portal_nome]["descartados"] += 1
                obs.evento(
                    "registro_descartado",
                    {
                        "portal": portal_nome,
                        "link": anuncio.get("link"),
                        "motivos": ["dados_insuficientes"] + qualidade.motivos,
                        "score_qualidade": qualidade.score,
                    },
                )
                continue

            if qualidade.bloquear:
                print("Registro bloqueado por baixa qualidade:", anuncio["link"])
                descartados += 1
                metricas_portal[portal_nome]["descartados"] += 1
                obs.evento(
                    "registro_descartado",
                    {
                        "portal": portal_nome,
                        "link": anuncio.get("link"),
                        "motivos": ["baixa_qualidade"] + qualidade.motivos,
                        "score_qualidade": qualidade.score,
                    },
                )
                continue

            imoveis_capturados.append(imovel)
            metricas_portal[portal_nome]["processados"] += 1

            if salvar_imovel(imovel):

                salvos += 1
                metricas_portal[portal_nome]["salvos"] += 1

            processados += 1



    finally:

        navegador.fechar()



    print(

        "Novos imóveis salvos:",

        salvos

    )

    _emitir_progresso(progress_callback, "exportacao", 85, "Gerando planilha de exportação...")


    caminho_excel = exportar_excel(imoveis_capturados)

    print(

        "Planilha gerada em:",

        caminho_excel

    )

    _emitir_progresso(progress_callback, "dashboard", 95, "Atualizando dashboard HTML...")

    caminho_dashboard = gerar_html_dashboard(tom_ia=tom_ia)
    print(
        "Dashboard HTML atualizado em:",
        caminho_dashboard
    )

    _emitir_progresso(progress_callback, "dashboard", 100, "Pipeline concluído.")

    qualidade_media = round(soma_score_qualidade / total_score_qualidade, 2) if total_score_qualidade else 0

    obs.evento(
        "fim_execucao",
        {
            "anuncios_capturados": len(anuncios),
            "imoveis_processados": len(imoveis_capturados),
            "novos_salvos": salvos,
            "descartados": descartados,
            "falhas_abertura": falhas_abertura,
            "higienizados": atualizados,
            "score_qualidade_medio": qualidade_media,
            "metricas_por_portal": metricas_portal,
            "arquivo_excel": str(caminho_excel),
            "arquivo_dashboard": str(caminho_dashboard),
            "tom_ia": tom_ia,
        },
    )

    resumo = {
        "run_id": run_id,
        "anuncios_capturados": len(anuncios),
        "imoveis_processados": len(imoveis_capturados),
        "novos_salvos": salvos,
        "descartados": descartados,
        "falhas_abertura": falhas_abertura,
        "higienizados": atualizados,
        "score_qualidade_medio": qualidade_media,
        "metricas_por_portal": metricas_portal,
        "arquivo_excel": str(caminho_excel),
        "arquivo_dashboard": str(caminho_dashboard),
        "tom_ia": tom_ia,
    }

    return resumo