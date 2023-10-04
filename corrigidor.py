""" engroossar linhas """

import cv2
from sys import argv
from imagem import *
from funcoes import *
import numpy as np

# python corrigidor.py arquivo destino gabarito
if len(argv) != 3:
    print(
        "Uso incorreto! Uso correto: python corrigidor.py imagem_de_entrada.jpeg diretorio_destino"
    )

imagem_original = abre_imagem(argv[1])
imagem_pb = deixa_imagem_preto_e_branco(imagem_original)
funcao_linha_baixo = pega_funcao_linha_de_baixo(imagem_pb, offset=147)
funcao_linha_meio = pega_funcao_linha_meio(funcao_linha_baixo, imagem_pb)
funcao_linha_cima = pega_funcao_linha_cima(
    funcao_linha_baixo, funcao_linha_meio, imagem_pb
)

# pega pontos iniciais e finais da linha de baixo - DEBUG
dim_imagem = imagem_pb.shape
pt1b = (0, funcao_linha_baixo(0))
pt2b = (dim_imagem[1] - 1, funcao_linha_baixo(dim_imagem[1] - 1))
# traça linha encima da linha de baixo - DEBUG
cv2.line(imagem_original, pt1b, pt2b, (0, 0, 255), 1)

# traça linha encima da linha do meio - DEBUG
pt1m = (int(funcao_linha_meio(0)), 0)
pt2m = (int(funcao_linha_meio(dim_imagem[0] - 1)), dim_imagem[0] - 1)
cv2.line(imagem_original, pt1m, pt2m, (0, 255, 0), 1)

# traça linha encima da linha de cima - DEBUG
pt1c = (0, funcao_linha_cima(0))
pt2c = (dim_imagem[1] - 1, funcao_linha_cima(dim_imagem[1] - 1))
cv2.line(imagem_original, pt1c, pt2c, (255, 0, 0), 1)

# acha interseccao entre linha do meio e linha de cima
intersection = acha_interseccao_entre_linhas(
    funcao_linha_cima, funcao_linha_meio, dim_imagem[1], dim_imagem[0]
)

# determina distancia media entre linhas gabarito
media = calcula_distancia_media_entre_linha_cima_e_baixo(
    funcao_linha_baixo, funcao_linha_cima, dim_imagem[1]
)

alternativas_marcadas = []
pontos_alternativas = []
for i in range(90):
    ponto_questao = devolve_posicao_ponto_para_questao(i, intersection, media)
    alternativa, ponto_alternativa = devolve_alternativa_marcada(
        ponto_questao, imagem_pb, media
    )
    alternativas_marcadas.append(alternativa)
    pontos_alternativas.append(ponto_alternativa)

for i in range(90):
    print(f"Questão {i+1}: {alternativas_marcadas[i]}")
    cv2.circle(imagem_original, pontos_alternativas[i], 5, (255, 0, 0), 5)

cv2.imshow("0", imagem_original[900:])
cv2.waitKey(0)
