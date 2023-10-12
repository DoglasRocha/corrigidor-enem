import cv2
from sys import argv
from imagem import *
import os
from funcoes_deteccao_questoes import *
from geracao_relatorio import *

# python corrigidor.py arquivo # gabarito
assert (
    len(argv) == 3
), "Uso incorreto! Uso correto: python corrigidor.py imagem_de_entrada.jpeg diretorio_destino"
assert os.path.isfile(argv[1]), "Imagem de entrada passada incorretamente"
assert os.path.isdir(argv[2]), "Diretório de destino passado incorretamente"

imagem_original = abre_imagem(argv[1])
imagem_pb = deixa_imagem_preto_e_branco(imagem_original)
(
    alternativas_marcadas,
    pontos_alternativas,
) = encontra_alternativas_marcadas_de_uma_prova(imagem_original, imagem_pb)

# relatório e marcação dos pontos encontrados
gerar_relatorio_pdf(
    imagem_original, 99, alternativas_marcadas, pontos_alternativas, argv[2]
)
# mostra_imagem(imagem_pb[900:])
