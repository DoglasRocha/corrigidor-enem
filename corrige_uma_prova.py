import os
from sys import argv
from imagem import *
from funcoes_deteccao_questoes import encontra_alternativas_marcadas_de_uma_prova
from geracao_relatorio import *
from corretor import *

# python corrigidor.py arquivo # gabarito
assert (
    len(argv) == 4
), "Uso incorreto! Uso correto: python corrigidor.py imagem_de_entrada.jpeg diretorio_destino diretorio_gabaritos"
assert os.path.isfile(argv[1]), "Imagem de entrada passada incorretamente"
assert os.path.isdir(argv[2]), "Diretório de destino passado incorretamente"
assert os.path.isdir(argv[3]), "Diretório de gabaritos passado incorretamente"

imagem_original = abre_imagem(argv[1])
pdf = canvas.Canvas(f"{argv[2]}/relatorio_prova_individual.pdf", pagesize=A4)

imagem_pb = deixa_imagem_preto_e_branco(imagem_original)
(
    alternativas_marcadas,
    pontos_alternativas,
) = encontra_alternativas_marcadas_de_uma_prova(imagem_original, imagem_pb)

gabaritos = abre_gabaritos(argv[3])
correcao = corrige_prova(alternativas_marcadas, gabaritos)
acertos_por_materia, qtd_questoes_materia = avalia_acertos_por_materia(correcao)

# relatório e marcação dos pontos encontrados
gerar_relatorio_pdf(
    imagem_original,
    99,
    alternativas_marcadas,
    pontos_alternativas,
    pdf,
    correcao,
    acertos_por_materia,
    qtd_questoes_materia,
)
# mostra_imagem(imagem_pb[900:])

pdf.save()
