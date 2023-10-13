from cv2 import Mat, circle
from imagem import salvar_imagem
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from PIL import Image


def gerar_imagem_relatorio(
    imagem_original: Mat, pontos_alternativas: list, correcao: list
) -> Mat:
    VERDE = (0, 255, 0)
    AMARELO = (255, 255, 0)
    VERMELHO = (255, 0, 0)

    for i in range(90):
        if len(correcao[i]) == 1:
            alternativa = correcao[i][0]
            circle(
                imagem_original,
                pontos_alternativas[i],
                5,
                VERDE if alternativa["Correção"] == "C" else VERMELHO,
                5,
            )
        else:
            cor = None
            if correcao[i][0]["Correção"] == "C" and correcao[i][1]["Correção"] == "C":
                cor = VERDE
            elif (
                correcao[i][0]["Correção"] == "E" and correcao[i][1]["Correção"] == "E"
            ):
                cor = VERMELHO
            else:
                cor = AMARELO
            circle(
                imagem_original,
                pontos_alternativas[i],
                5,
                cor,
                5,
            )

    return imagem_original


def gerar_relatorio_marcacoes(
    numero_prova: int, alternativas_marcadas: list, correcao: list
) -> str:
    texto_relatorio = f"RELATÓRIO PROVA {numero_prova}:\n"
    texto_relatorio += "\tCaso a questão seja de língua estrangeira, primero será apresentada a correção em espanhol e depois em inglês.\n\n"
    for i in range(15):
        for j in range(6):
            texto_relatorio += (
                f"Questão {i+1 + j * 15:2d}: ({alternativas_marcadas[i + j * 15]}) "
            )
            if len(correcao[i + j * 15]) == 1:
                texto_relatorio += f'{correcao[i + j * 15][0]["Correção"]} '
            else:
                texto_relatorio += f'{correcao[i + j * 15][0]["Correção"]}/{correcao[i + j * 15][1]["Correção"]} '

            texto_relatorio += "| "

        texto_relatorio += "\t\n"

    texto_relatorio += (
        "\n\tLegenda: Questão XX: (alternativa marcada) C - Certo, E - Errado\n"
    )
    """with open(f"{path_dir_saida}/relatorio_prova_{numero_prova}.txt", "w") as arquivo:
        arquivo.write(texto_relatorio)"""

    return texto_relatorio


def gerar_relatorio_correcao(correcao):
    materias = {
        "Biologia": 0,
        "Espanhol": 0,
        "Filosofia": 0,
        "Física": 0,
        "Geografia": 0,
        "História": 0,
        "Inglês": 0,
        "Língua Portuguesa": 0,
        "Matemática": 0,
        "Química": 0,
        "Sociologia": 0,
    }

    questoes_por_materia = {
        "Biologia": 0,
        "Espanhol": 0,
        "Filosofia": 0,
        "Física": 0,
        "Geografia": 0,
        "História": 0,
        "Inglês": 0,
        "Língua Portuguesa": 0,
        "Matemática": 0,
        "Química": 0,
        "Sociologia": 0,
    }

    for linha in correcao:
        for celula in linha:
            if celula["Correção"] == "C":
                materias[celula["Matéria"]] += 1
            questoes_por_materia[celula["Matéria"]] += 1

    texto = "\n\n\nRELATÓRIO QUANTITATIVO:\n\tAcertos por matéria:\n"
    acertos_caso_espanhol = 0
    acertos_caso_ingles = 0
    for key, value in materias.items():
        texto += f"\t\t{key}: {value}/{questoes_por_materia[key]}\n"
        acertos_caso_espanhol += value if key != "Inglês" else 0
        acertos_caso_ingles += value if key != "Espanhol" else 0

    texto += "\n\nAcertos gerais:\n"
    texto += f"\tCaso Espanhol: {acertos_caso_espanhol}/90\n\tCaso Inglês: {acertos_caso_ingles}/90\n\n"

    return texto


def gerar_relatorio_de_erro(numero_prova: int, erro: Exception) -> str:
    texto_relatorio = (
        f"RELATÓRIO PROVA {numero_prova}:\n" + f"\tDeu merda. Erro: {str(erro)}\n"
    )
    """with open(f"{path_dir_saida}/relatorio_prova_{numero_prova}.txt", "w") as arquivo:
        arquivo.write(texto_relatorio)"""

    return texto_relatorio


def gerar_relatorio_pdf(
    imagem_original: Mat,
    numero_prova: int,
    alternativas_marcadas: list,
    pontos_alternativas: list,
    pdf: canvas.Canvas,
    correcao: list,
) -> None:
    relatorio_marcacoes = gerar_relatorio_marcacoes(
        numero_prova, alternativas_marcadas, correcao
    )
    relatorio_correcao = gerar_relatorio_correcao(correcao)

    texto_geral = relatorio_marcacoes + relatorio_correcao
    # gera img relatorio e converte para PIL
    imagem_resultante = gerar_imagem_relatorio(
        imagem_original, pontos_alternativas, correcao
    )
    img = Image.fromarray(imagem_resultante)

    # desenha imagem
    pdf.drawInlineImage(img, 0, 0, *A4)
    pdf.showPage()

    # desenha texto
    pdf.setFontSize(9)
    texto_objeto = pdf.beginText(2 * cm, 27.7 * cm)
    for linha in texto_geral.replace("\t", "    ").split("\n"):
        texto_objeto.textLine(linha)
    pdf.drawText(texto_objeto)
    pdf.showPage()


def gerar_relatorio_pdf_de_erro(
    imagem_original: Mat,
    numero_prova: int,
    E: Exception,
    pdf: canvas.Canvas,
) -> None:
    # converte imagem cv2 para PIL
    img = Image.fromarray(imagem_original)

    # desenha imagem no pdf
    pdf.drawInlineImage(img, 0, 0, *A4)
    pdf.showPage()

    # desenha texto
    texto_relatorio = gerar_relatorio_de_erro(numero_prova, E)
    pdf.setFontSize(10)
    texto_objeto = pdf.beginText(2 * cm, 27.7 * cm)
    for linha in texto_relatorio.replace("\t", "    ").split("\n"):
        texto_objeto.textLine(linha)
    pdf.drawText(texto_objeto)
    pdf.showPage()
