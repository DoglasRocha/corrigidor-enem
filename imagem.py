import cv2
from cv2 import Mat


def abre_imagem(path: str) -> Mat:
    return cv2.imread(path)


def deixa_imagem_preto_e_branco(img: Mat) -> Mat:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)

    return img


def salvar_imagem(img: Mat, path: str) -> None:
    cv2.imwrite(path, img)


def mostra_imagem(img: Mat) -> None:
    cv2.imshow("img", img)
    cv2.waitKey(0)
