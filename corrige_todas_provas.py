import cv2
from sys import argv
from imagem import *
import os
from funcoes import *

# python corrigidor.py diretorio_entrada diretorio_destino # gabarito
assert (
    len(argv) == 3
), "Uso incorreto! Uso correto: python corrigidor.py imagem_de_entrada.jpeg diretorio_destino"
assert os.path.isdir(argv[1]), "Diretório de entrada passado incorretamente"
assert os.path.isdir(argv[2]), "Diretório de destino passado incorretamente"

path_imagens = os.listdir(argv[1])
for n_path_imagem in range(len(path_imagens)):
    try:
        imagem_original = abre_imagem(f"{argv[1]}/{path_imagens[n_path_imagem]}")
        imagem_pb = deixa_imagem_preto_e_branco(imagem_original)
        (
            alternativas_marcadas,
            pontos_alternativas,
        ) = encontra_alternativas_marcadas_de_uma_prova(imagem_original, imagem_pb)

        # relatório e marcação dos pontos encontrados
        with open(f"{argv[2]}/relatorio_prova_{n_path_imagem}.txt", "w") as arquivo:
            arquivo.write(f"RELATÓRIO PROVA {n_path_imagem}:\n")
            for i in range(90):
                arquivo.write(f"\tQuestão {i+1}: {alternativas_marcadas[i]}")
                cv2.circle(imagem_original, pontos_alternativas[i], 5, (255, 0, 0), 5)
                if (i + 1) % 6 == 0:
                    arquivo.write("\n")

        salvar_imagem(imagem_original, f"{argv[2]}/prova_{n_path_imagem}.jpg")
        # salvar_imagem(imagem_pb, f"{argv[2]}/prova_{n_path_imagem}_pb.jpg")
    except Exception as E:
        with open(f"{argv[2]}/relatorio_prova_{n_path_imagem}.txt", "w") as arquivo:
            arquivo.write(f"RELATÓRIO PROVA {n_path_imagem}:")
            arquivo.write(f"Deu merda. Erro: {str(E)}")
