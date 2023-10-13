import os
from sys import argv
from imagem import *
from funcoes_deteccao_questoes import encontra_alternativas_marcadas_de_uma_prova
from geracao_relatorio import *
from corretor import *

# python corrigidor.py diretorio_entrada diretorio_destino # gabarito
assert (
    len(argv) == 4
), "Uso incorreto! Uso correto: python corrigidor.py imagem_de_entrada.jpeg diretorio_destino diretorio_gabaritos"
assert os.path.isdir(argv[1]), "Diretório de entrada passado incorretamente"
assert os.path.isdir(argv[2]), "Diretório de destino passado incorretamente"
assert os.path.isdir(argv[3]), "Diretório de gabaritos passado incorretamente"

path_imagens = os.listdir(argv[1])
pdf = canvas.Canvas(f"{argv[2]}/relatorio_provas.pdf", pagesize=A4)
gabaritos = abre_gabaritos(argv[3])

for n_path_imagem in range(len(path_imagens)):
    try:
        imagem_original = abre_imagem(f"{argv[1]}/{path_imagens[n_path_imagem]}")
        imagem_pb = deixa_imagem_preto_e_branco(imagem_original)
        (
            alternativas_marcadas,
            pontos_alternativas,
        ) = encontra_alternativas_marcadas_de_uma_prova(imagem_original, imagem_pb)

        correcao = corrige_prova(alternativas_marcadas, gabaritos)

        # relatório e marcação dos pontos encontrados
        gerar_relatorio_pdf(
            imagem_original,
            n_path_imagem,
            alternativas_marcadas,
            pontos_alternativas,
            pdf,
            correcao,
        )
    except Exception as E:
        gerar_relatorio_pdf_de_erro(imagem_original, n_path_imagem, E, pdf)

pdf.save()
