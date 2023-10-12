from cv2 import Mat, circle
from imagem import salvar_imagem


def gerar_relatorio(
    imagem_original: Mat,
    numero_prova: int,
    alternativas_marcadas: list,
    pontos_alternativas: list,
    path_dir_saida: str,
) -> None:
    texto_relatorio = f"RELATÓRIO PROVA {numero_prova}:\n"
    for i in range(15):
        for j in range(6):
            texto_relatorio += (
                f"\tQuestão {i+1 + j * 15}: {alternativas_marcadas[i + j * 15]}"
            )
            circle(
                imagem_original,
                pontos_alternativas[i + j * 15],
                5,
                (255, 0, 0),
                5,
            )
        texto_relatorio += "\n"

    with open(f"{path_dir_saida}/relatorio_prova_{numero_prova}.txt", "w") as arquivo:
        arquivo.write(texto_relatorio)

    salvar_imagem(imagem_original, f"{path_dir_saida}/prova_{numero_prova}.jpg")


def gerar_relatorio_de_erro(
    numero_prova: int, path_dir_saida: str, erro: Exception
) -> None:
    with open(f"{path_dir_saida}/relatorio_prova_{numero_prova}.txt", "w") as arquivo:
        arquivo.write(f"RELATÓRIO PROVA {numero_prova}:\n")
        arquivo.write(f"\tDeu merda. Erro: {str(erro)}\n")
