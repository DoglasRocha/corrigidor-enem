from sys import argv
from imagem import *
import os
from funcoes_deteccao_questoes import *
from geracao_relatorio import *

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
        gerar_relatorio(
            imagem_original,
            n_path_imagem,
            alternativas_marcadas,
            pontos_alternativas,
            argv[2],
        )
    except Exception as E:
        gerar_relatorio_de_erro(n_path_imagem, argv[2], E)
