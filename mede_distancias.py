# programa criado para medir distancias entre as linhas dos gabaritos
from sys import argv
from imagem import *
from funcoes_deteccao_questoes import *
import os

# python corrigidor.py arquivo destino gabarito
if len(argv) != 2:
    print("Uso incorreto! Uso correto: python mede_distancia.py diretorio_entrada")

if not os.path.exists(argv[1]):
    print("Diretório não existente!!")
    exit(1)

medias = []

for image_path in sorted(os.listdir(argv[1])):
    imagem_original = abre_imagem(f"./{argv[1]}/{image_path}")
    imagem_pb = deixa_imagem_preto_e_branco(imagem_original)
    funcao_linha_baixo = pega_funcao_linha_de_baixo(imagem_pb)
    funcao_linha_meio = pega_funcao_linha_meio(funcao_linha_baixo, imagem_pb)
    funcao_linha_cima = pega_funcao_linha_cima(
        funcao_linha_baixo, funcao_linha_meio, imagem_pb
    )

    # determina distancia media entre linhas gabarito
    dim_imagem = imagem_pb.shape
    media = calcula_distancia_media_entre_linha_cima_e_baixo(
        funcao_linha_baixo, funcao_linha_cima, dim_imagem[1]
    )
    medias.append(media)

    print("Nome arquivo: {}, média da distância: {}".format(image_path, media))

medias_aceitaveis = list(filter(lambda x: x > 500, medias))
print(f"Valor máximo: {max(medias_aceitaveis)}, valor mínimo: {min(medias_aceitaveis)}")
print(f"Provas descartadas: {len(medias) - len(medias_aceitaveis)}")
