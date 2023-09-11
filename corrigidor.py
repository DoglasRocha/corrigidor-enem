import cv2
from sys import argv
from imagem import *
from funcoes import *
import numpy as np

# python corrigidor.py arquivo destino gabarito
if (len(argv) != 3):
    print("Uso incorreto! Uso correto: python corrigidor.py imagem_de_entrada.jpeg diretorio_destino")

imagem_original = abre_imagem(argv[1])
imagem_pb = deixa_imagem_preto_e_branco(imagem_original)
funcao_linha_baixo = pega_equacao_linha_de_baixo(imagem_pb)

# pega pontos iniciais e finais da linha de baixo - DEBUG
dim_imagem = imagem_pb.shape
pt1 = (0, funcao_linha_baixo(0))
pt2 = (dim_imagem[1] - 1, funcao_linha_baixo(dim_imagem[1] - 1))

# traça linha encima da linha de baixo - DEBUG
cv2.line(imagem_original, pt1, pt2, (0, 0, 255), 2)

# traça linha encima da linha do meio - DEBUG
funcao_linha_meio = pega_equacao_linha_meio(funcao_linha_baixo, imagem_pb)
pt1 = (funcao_linha_meio(0), 0)
pt2 = (funcao_linha_meio(dim_imagem[0] - 1), dim_imagem[0] - 1)
cv2.line(imagem_original, pt1, pt2, (0, 255, 0), 2)

# traça linha encima da linha de cima - DEBUG
funcao_linha_cima = pega_equacao_linha_cima(funcao_linha_baixo, funcao_linha_meio, imagem_pb)
pt1 = (0, funcao_linha_cima(0))
pt2 = (dim_imagem[1] - 1, funcao_linha_cima(dim_imagem[1] - 1))
cv2.line(imagem_original, pt1, pt2, (255, 0, 0), 2)

# determina distancia media entre linhas gabarito
media = 0
for i in range(dim_imagem[1]):
    media += (funcao_linha_baixo(i) - funcao_linha_cima(i)) / dim_imagem[1]
media = round(media)

# traça linha suposta para coluna de opcoes a de 1 a 15
PROPORCAO = 483 / 457
pt1 = (round(funcao_linha_meio(0) - media * PROPORCAO), 0)
pt2 = (round(funcao_linha_meio(dim_imagem[0] - 1) - media * PROPORCAO), dim_imagem[0] - 1)
cv2.line(imagem_original, pt1, pt2, (0, 255, 255), 2)

cv2.imwrite("desgraca.png", imagem_pb)
cv2.imshow("0", imagem_original[600:])
cv2.waitKey(0)
