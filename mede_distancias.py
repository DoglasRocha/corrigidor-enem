# programa criado para medir distancias entre as linhas dos gabaritos
import cv2
from sys import argv
from imagem import *
from funcoes import *
import os

# python corrigidor.py arquivo destino gabarito
if (len(argv) != 2):
    print("Uso incorreto! Uso correto: python mede_distancia.py diretorio_entrada")
    
if not os.path.exists(argv[1]):
    print("Diretório não existente!!")
    exit(1)

medias = []
    
for image_path in sorted(os.listdir(argv[1])):

    imagem_original = abre_imagem(f'./{argv[1]}/{image_path}')
    imagem_pb = deixa_imagem_preto_e_branco(imagem_original)
    funcao_linha_baixo = pega_funcao_linha_de_baixo(imagem_pb)
    funcao_linha_meio = pega_funcao_linha_meio(funcao_linha_baixo, imagem_pb)
    funcao_linha_cima = pega_funcao_linha_cima(funcao_linha_baixo, funcao_linha_meio, imagem_pb)

    # pega pontos iniciais e finais da linha de baixo - DEBUG
    dim_imagem = imagem_pb.shape
    pt1 = (0, funcao_linha_baixo(0))
    pt2 = (dim_imagem[1] - 1, funcao_linha_baixo(dim_imagem[1] - 1))

    # traça linha encima da linha de baixo - DEBUG
    cv2.line(imagem_original, pt1, pt2, (0, 0, 255), 2)

    # traça linha encima da linha do meio - DEBUG
    pt1 = (int(funcao_linha_meio(0)), 0)
    pt2 = (int(funcao_linha_meio(dim_imagem[0] - 1)), dim_imagem[0] - 1)
    cv2.line(imagem_original, pt1, pt2, (0, 255, 0), 2)

    # traça linha encima da linha de cima - DEBUG
    pt1 = (0, funcao_linha_cima(0))
    pt2 = (dim_imagem[1] - 1, funcao_linha_cima(dim_imagem[1] - 1))
    cv2.line(imagem_original, pt1, pt2, (255, 0, 0), 2)

    # determina distancia media entre linhas gabarito
    media = 0 
    media = (
        (funcao_linha_baixo(0) - funcao_linha_cima(0)) +
        (funcao_linha_baixo(dim_imagem[1] - 1) - funcao_linha_cima(dim_imagem[1] - 1))
    ) / 2
    media = round(media)
    medias.append(media)
    
    print("Nome arquivo: {}, média da distância: {}".format(image_path, media))
    
medias = list(filter(lambda x : x > 500, medias))
print(f'Valor máximo: {max(medias)}, valor mínimo: {min(medias)}')