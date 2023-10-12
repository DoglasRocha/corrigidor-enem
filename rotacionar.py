# programa criado para rotacionar as imagens dos gabaritos
import cv2
from sys import argv
from imagem import *
from funcoes_deteccao_questoes import *
import os

if len(argv) != 3:
    print(
        f"Uso incorreto! Uso correto: python {argv[0]} diretorio_entrada diretorio_saida"
    )

if not os.path.exists(argv[1]) or not os.path.exists(argv[2]):
    print("Diretório não existente!!")
    exit(1)

for image_path in os.listdir(argv[1]):
    img = abre_imagem(f"{argv[1]}/{image_path}")
    img = cv2.rotate(img, cv2.ROTATE_180)
    salvar_imagem(img, f"{argv[2]}/{image_path}")
