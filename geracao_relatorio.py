from cv2 import Mat, circle
from imagem import salvar_imagem
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from PIL import Image


def gerar_texto_e_imagem_relatorio(
    imagem_original: Mat,
    numero_prova: int,
    alternativas_marcadas: list,
    pontos_alternativas: list,
) -> None:
    texto_relatorio = f"RELATÓRIO PROVA {numero_prova}:\n"
    for i in range(15):
        for j in range(6):
            texto_relatorio += (
                f"Questão {i+1 + j * 15:2d}: {alternativas_marcadas[i + j * 15]}\t"
            )
            circle(
                imagem_original,
                pontos_alternativas[i + j * 15],
                5,
                (255, 0, 0),
                5,
            )
        texto_relatorio += "\n"

    """with open(f"{path_dir_saida}/relatorio_prova_{numero_prova}.txt", "w") as arquivo:
        arquivo.write(texto_relatorio)

    salvar_imagem(imagem_original, f"{path_dir_saida}/prova_{numero_prova}.jpg")"""

    return texto_relatorio, imagem_original


def gerar_relatorio_de_erro(numero_prova: int, erro: Exception) -> None:
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
) -> None:
    texto_relatorio, imagem_resultante = gerar_texto_e_imagem_relatorio(
        imagem_original,
        numero_prova,
        alternativas_marcadas,
        pontos_alternativas,
    )

    # converte imagem cv2 para PIL
    img = Image.fromarray(imagem_resultante)

    # desenha imagem
    pdf.drawInlineImage(img, 0, 0, *A4)
    pdf.showPage()

    # desenha texto
    pdf.setFontSize(10)
    texto_objeto = pdf.beginText(2 * cm, 27.7 * cm)
    for linha in texto_relatorio.replace("\t", "    ").split("\n"):
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
