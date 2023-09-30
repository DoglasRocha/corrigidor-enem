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
funcao_linha_meio = pega_equacao_linha_meio(funcao_linha_baixo, imagem_pb)
funcao_linha_cima = pega_equacao_linha_cima(funcao_linha_baixo, funcao_linha_meio, imagem_pb)

# pega pontos iniciais e finais da linha de baixo - DEBUG
dim_imagem = imagem_pb.shape
pt1 = (0, funcao_linha_baixo(0))
pt2 = (dim_imagem[1] - 1, funcao_linha_baixo(dim_imagem[1] - 1))
# traça linha encima da linha de baixo - DEBUG
cv2.line(imagem_original, pt1, pt2, (0, 0, 255), 1)

# traça linha encima da linha do meio - DEBUG
pt1 = (funcao_linha_meio(0), 0)
pt2 = (funcao_linha_meio(dim_imagem[0] - 1), dim_imagem[0] - 1)
cv2.line(imagem_original, pt1, pt2, (0, 255, 0), 1)

# traça linha encima da linha de cima - DEBUG
pt1 = (0, funcao_linha_cima(0))
pt2 = (dim_imagem[1] - 1, funcao_linha_cima(dim_imagem[1] - 1))
cv2.line(imagem_original, pt1, pt2, (255, 0, 0), 1)

# determina distancia media entre linhas gabarito
media = 0
y_max = 0
y_min = 99999
for i in range(dim_imagem[1]):
    baixo = funcao_linha_baixo(i)
    cima = funcao_linha_cima(i)
    media += (baixo - cima) / dim_imagem[1]
    y_min = baixo if baixo < y_min else y_min
    y_max = cima if cima > y_max else y_max

# traça linha suposta para coluna de opcoes a de 1 a 15
PROPORCAO = 1.0579888265494013
pt1 = (round(funcao_linha_meio(y_min) - media * PROPORCAO), y_min)
pt2 = (round(funcao_linha_meio(y_max) - media * PROPORCAO), y_max)
cv2.line(imagem_original, pt1, pt2, (0, 255, 255), 1)

cv2.imshow("0", imagem_original[900:])
cv2.waitKey(0)
