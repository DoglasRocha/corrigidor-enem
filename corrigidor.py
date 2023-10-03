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
pt1 = (0, funcao_linha_baixo(0))
pt2 = (dim_imagem[1] - 1, funcao_linha_baixo(dim_imagem[1] - 1))
# traça linha encima da linha de baixo - DEBUG
cv2.line(imagem_original, pt1, pt2, (0, 0, 255), 1)

# traça linha encima da linha do meio - DEBUG
pt1 = (int(funcao_linha_meio(0)), 0)
pt2 = (int(funcao_linha_meio(dim_imagem[0] - 1)), dim_imagem[0] - 1)
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
PROPORCAO_1_A_15 = -0.8413547237076648
pt1 = (round(funcao_linha_meio(y_min) + media * PROPORCAO_1_A_15), y_min)
pt2 = (round(funcao_linha_meio(y_max) + media * PROPORCAO_1_A_15), y_max)
cv2.line(imagem_original, pt1, pt2, (0, 255, 255), 2)

# traça linha suposta para coluna de opcoes a de 16 a 30
PROPORCAO_16_A_30 = -0.5365418894830659
pt1 = (round(funcao_linha_meio(y_min) + media * PROPORCAO_16_A_30), y_min)
pt2 = (round(funcao_linha_meio(y_max) + media * PROPORCAO_16_A_30), y_max)
cv2.line(imagem_original, pt1, pt2, (0, 255, 255), 2)

# traça linha suposta para coluna de opções a de 31 a 45
PROPORCAO_31_A_45 = -0.2281639928698752
pt1 = (round(funcao_linha_meio(y_min) + media * PROPORCAO_31_A_45), y_min)
pt2 = (round(funcao_linha_meio(y_max) + media * PROPORCAO_31_A_45), y_max)
cv2.line(imagem_original, pt1, pt2, (0, 255, 255), 2)

# traça linha suposta para coluna de opcoes a de 46 a 60
PROPORCAO_46_A_60 = 0.09803921568627451
pt1 = (round(funcao_linha_meio(y_min) + media * PROPORCAO_46_A_60), y_min)
pt2 = (round(funcao_linha_meio(y_max) + media * PROPORCAO_46_A_60), y_max)
cv2.line(imagem_original, pt1, pt2, (0, 255, 255), 2)

# traça linha suposta para coluna de opcoes a de 61 a 75
PROPORCAO_61_A_75 = 0.40641711229946526
pt1 = (round(funcao_linha_meio(y_min) + media * PROPORCAO_61_A_75), y_min)
pt2 = (round(funcao_linha_meio(y_max) + media * PROPORCAO_61_A_75), y_max)
cv2.line(imagem_original, pt1, pt2, (0, 255, 255), 2)

# traça linha suposta para coluna de opcoes a de 76 a 90
PROPORCAO_76_A_90 = 0.7165775401069518
pt1 = (round(funcao_linha_meio(y_min) + media * PROPORCAO_76_A_90), y_min)
pt2 = (round(funcao_linha_meio(y_max) + media * PROPORCAO_76_A_90), y_max)
cv2.line(imagem_original, pt1, pt2, (0, 255, 255), 2)

# traça linha suposta para linha contendo questoes {1,16,31,46,61,76}
PROPORCAO_PRIMEIRA_LINHA = 0.14616755793226383
pt1 = (0, round(funcao_linha_cima(0) + media * PROPORCAO_PRIMEIRA_LINHA))
pt2 = (
    dim_imagem[1] - 1,
    round(funcao_linha_cima(dim_imagem[1] - 1) + media * PROPORCAO_PRIMEIRA_LINHA),
)
cv2.line(imagem_original, pt1, pt2, (255, 255, 0), 2)

# teste se proporcoes entre linhas e colunas funcionam
PROPORCAO_ENTRE_ALTERNATIVAS_X = 0.04634581105169341
PROPORCAO_ENTRE_ALTERNATIVAS_Y = 0.0570409982174688
# traça linha suposta para coluna de opcoes b de 1 a 15
PROPORCAO_1_A_15 = -0.8413547237076648
pt1 = (
    round(
        funcao_linha_meio(y_min)
        + media * PROPORCAO_1_A_15
        + media * PROPORCAO_ENTRE_ALTERNATIVAS_X
    ),
    y_min,
)
pt2 = (
    round(
        funcao_linha_meio(y_max)
        + media * PROPORCAO_1_A_15
        + media * PROPORCAO_ENTRE_ALTERNATIVAS_X
    ),
    y_max,
)
cv2.line(imagem_original, pt1, pt2, (75, 255, 150), 2)

# traça linha suposta para linha contendo questoes {2,17,32,47,62,77}
PROPORCAO_PRIMEIRA_LINHA = 0.14616755793226383
pt1 = (
    0,
    round(
        funcao_linha_cima(0)
        + media * PROPORCAO_PRIMEIRA_LINHA
        + media * PROPORCAO_ENTRE_ALTERNATIVAS_Y
    ),
)
pt2 = (
    dim_imagem[1] - 1,
    round(
        funcao_linha_cima(dim_imagem[1] - 1)
        + media * PROPORCAO_PRIMEIRA_LINHA
        + media * PROPORCAO_ENTRE_ALTERNATIVAS_Y
    ),
)
cv2.line(imagem_original, pt1, pt2, (175, 255, 0), 2)

cv2.imshow("0", imagem_original[900:])
cv2.waitKey(0)
