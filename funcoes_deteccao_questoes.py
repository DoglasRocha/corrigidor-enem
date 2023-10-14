import cv2
from typing import Callable


def faz_funcao_da_reta_para_x(pos_linhas: list, pos_colunas: list) -> Callable:
    m = (pos_linhas[0] - pos_linhas[1]) / (pos_colunas[0] - pos_colunas[1])

    return lambda x: int(round(m * x - m * pos_colunas[0] + pos_linhas[0]))


def faz_funcao_da_reta_para_y(pos_linhas: list, pos_colunas: list) -> Callable:
    if pos_colunas[0] - pos_colunas[1] == 0:
        return lambda y: pos_colunas[0]

    m = (pos_linhas[0] - pos_linhas[1]) / (pos_colunas[0] - pos_colunas[1])

    return lambda y: int(round((y + m * pos_colunas[0] - pos_linhas[0]) / m))


def pega_funcao_linha_de_baixo(imagem_pb: cv2.Mat, offset: int = 70) -> Callable:
    tam_y, tam_x = imagem_pb.shape
    pos_colunas = [offset, tam_x - offset]
    pos_linhas = [-1, -1]

    for i in range(len(pos_colunas)):
        for j in range(tam_y - 25, 0, -1):
            if imagem_pb[j][pos_colunas[i]] == 0:
                pos_linhas[i] = j
                break

    return faz_funcao_da_reta_para_x(pos_linhas, pos_colunas)


def pega_funcao_linha_meio(
    funcao_linha_baixo: Callable, imagem_pb: cv2.Mat
) -> Callable:
    tam_y, tam_x = imagem_pb.shape
    pos_colunas_esq = [tam_x // 2 - 100, -1]
    pos_colunas_dir = [tam_x // 2 + 100, -1]

    y1 = funcao_linha_baixo(pos_colunas_esq[0]) - 5

    # rotina para encontrar linha do meio
    for i in range(2):
        for j in range(pos_colunas_esq[0], tam_x):
            if imagem_pb[y1][j] == 0:
                pos_colunas_esq[i] = j
                y1 = y1 - 300
                break

    y2 = funcao_linha_baixo(pos_colunas_dir[0]) - 5
    for i in range(2):
        for j in range(pos_colunas_dir[0] + 6, 0, -1):
            if imagem_pb[y2][j] == 0:
                pos_colunas_dir[i] = j
                y2 = y2 - 300
                break

    # colunas da linha do meio serao a media das colunas da direita e da esquerda
    pos_colunas = [(pos_colunas_dir[i] + pos_colunas_esq[i]) / 2 for i in range(2)]

    return faz_funcao_da_reta_para_y(
        [(y1 + y2) / 2 + 600, (y1 + y2) / 2 + 300], pos_colunas
    )


def pega_funcao_linha_cima(
    funcao_linha_baixo: Callable, funcao_linha_meio: Callable, imagem_pb: cv2.Mat
) -> Callable:
    x_meio = imagem_pb.shape[1] // 2 - 100
    y_meio = funcao_linha_baixo(x_meio) - 5
    points_DEBUG = []

    # rotina para encontrar linha do meio
    for j in range(x_meio, imagem_pb.shape[1] - 1):
        if imagem_pb[y_meio][j] == 0:
            x_meio = j
            break

    y_baixo_meio = funcao_linha_baixo(x_meio)

    # rotina para acompanhar a linha do meio até sair
    y_quebra = -1
    for i in range(y_baixo_meio, 0, -20):
        points_DEBUG.append((funcao_linha_meio(i), i))
        if imagem_pb[i][int(funcao_linha_meio(i))] != 0:
            y_quebra = i
            break

    # rotina para achar linha de cima
    pos_colunas = [imagem_pb.shape[1] // 2 - 200, imagem_pb.shape[1] // 2 + 200]

    pos_linhas = [y_quebra, -1]

    for i in range(2):
        for j in range(y_quebra, imagem_pb.shape[0]):
            points_DEBUG.append((pos_colunas[i], j))
            if imagem_pb[j][pos_colunas[i]] == 0:
                pos_linhas[i] = j
                break

    """for point in points_DEBUG:
        cv2.circle(imagem_pb, point, 5, (0,0,0), 5)"""
    # cv2.imshow("a", imagem_pb[600:])
    # cv2.waitKey(0)

    return faz_funcao_da_reta_para_x(pos_linhas, pos_colunas)


def calcula_distancia_media_entre_linha_cima_e_baixo(
    funcao_linha_baixo: Callable, funcao_linha_cima: Callable, tam_x: int
) -> int:
    return round(
        (
            (funcao_linha_baixo(0) - funcao_linha_cima(0))
            + (funcao_linha_baixo(tam_x - 1) - funcao_linha_cima(tam_x - 1))
        )
        / 2
    )


def acha_interseccao_entre_linhas(
    funcao_linha_x: Callable, funcao_linha_y: Callable, tam_x_img: int, tam_y_img: int
) -> tuple[int, int]:
    for x in range(tam_x_img // 3, (2 * tam_x_img) // 3):
        for y in range(tam_y_img // 2, tam_y_img - 1):
            result = (x, round(funcao_linha_x(x)))
            if result == (round(funcao_linha_y(y)), y):
                return result

    return (-1, -1)


def devolve_posicao_ponto_para_questao(
    questao: int,
    interseccao_linhas: tuple,
    media: int,
    funcao_linha_cima: Callable = None,
) -> tuple:
    PROPORCOES_X = [
        -0.8413547237076648,  # PROPORCAO_1_A_15
        -0.5365418894830659,  # PROPORCAO_16_A_30
        -0.2281639928698752,  # PROPORCAO_31_A_45
        0.09803921568627451,  # PROPORCAO_46_A_60
        0.40641711229946526,  # PROPORCAO_61_A_75
        0.7165775401069518,  # PROPORCAO_76_A_90
    ]
    PROPORCAO_PRIMEIRA_LINHA = 0.14616755793226383
    PROPORCAO_ENTRE_ALTERNATIVAS_Y = 0.05614973262032086

    pos_x_questao = questao // 15
    pos_y_questao = questao % 15

    proporcao_x = PROPORCOES_X[pos_x_questao]
    x = interseccao_linhas[0] + media * proporcao_x
    y = None
    if funcao_linha_cima:
        y = (
            funcao_linha_cima(x)
            + media * PROPORCAO_PRIMEIRA_LINHA
            + media * pos_y_questao * PROPORCAO_ENTRE_ALTERNATIVAS_Y
        )
    else:
        y = (
            interseccao_linhas[1]
            + media * PROPORCAO_PRIMEIRA_LINHA
            + media * pos_y_questao * PROPORCAO_ENTRE_ALTERNATIVAS_Y
        )
    return (
        round(x),
        round(y),
    )


def devolve_alternativa_marcada(
    ponto_alternativa_a: tuple, img_pb: cv2.Mat, media: int
) -> tuple[str, tuple[int, int]]:
    alternativas = "abcde"
    ponto_encontrado = ()
    alternativa_encontrada = ""
    PROPORCAO_ENTRE_ALTERNATIVAS_X = 0.04634581105169341
    for i in range(len(alternativas)):
        x = round(ponto_alternativa_a[0] + media * PROPORCAO_ENTRE_ALTERNATIVAS_X * i)
        y = ponto_alternativa_a[1]
        if (
            img_pb[y][x] == 0
            and (
                img_pb[y + 5][x] == 0
                or img_pb[y - 5][x] == 0
                or img_pb[y][x + 5] == 0
                or img_pb[y][x - 5] == 0
            )
        ) or (
            img_pb[y + 5][x] == 0
            and img_pb[y - 5][x] == 0
            and img_pb[y][x + 5] == 0
            and img_pb[y][x - 5] == 0
        ):
            alternativa_encontrada += alternativas[i]
            ponto_encontrado = (x, y)
            cv2.circle(img_pb, (x, y), 2, (255, 255, 255))
            cv2.circle(img_pb, (x, y), 4, (0, 0, 0))

    return (
        ("?", (-1, -1))
        if len(alternativa_encontrada) != 1
        else (alternativa_encontrada, ponto_encontrado)
    )


def determina_linhas_de_guia(
    imagem_original: cv2.Mat, imagem_pb: cv2.Mat
) -> tuple[Callable, Callable, Callable]:
    funcao_linha_baixo = pega_funcao_linha_de_baixo(imagem_pb, offset=147)
    funcao_linha_meio = pega_funcao_linha_meio(funcao_linha_baixo, imagem_pb)
    funcao_linha_cima = pega_funcao_linha_cima(
        funcao_linha_baixo, funcao_linha_meio, imagem_pb
    )

    # pega pontos iniciais e finais da linha de baixo - DEBUG
    dim_imagem = imagem_pb.shape
    pt1b = (0, funcao_linha_baixo(0))
    pt2b = (dim_imagem[1] - 1, funcao_linha_baixo(dim_imagem[1] - 1))
    # traça linha encima da linha de baixo - DEBUG
    cv2.line(imagem_original, pt1b, pt2b, (0, 0, 255), 1)

    # traça linha encima da linha do meio - DEBUG
    pt1m = (int(funcao_linha_meio(0)), 0)
    pt2m = (int(funcao_linha_meio(dim_imagem[0] - 1)), dim_imagem[0] - 1)
    cv2.line(imagem_original, pt1m, pt2m, (0, 255, 0), 1)

    # traça linha encima da linha de cima - DEBUG
    pt1c = (0, funcao_linha_cima(0))
    pt2c = (dim_imagem[1] - 1, funcao_linha_cima(dim_imagem[1] - 1))
    cv2.line(imagem_original, pt1c, pt2c, (255, 0, 0), 1)

    return funcao_linha_baixo, funcao_linha_meio, funcao_linha_cima


def encontra_alternativas_marcadas_de_uma_prova(
    imagem_original: cv2.Mat, imagem_pb: cv2.Mat
) -> tuple[list, list]:
    dim_imagem = imagem_original.shape
    funcao_linha_baixo, funcao_linha_meio, funcao_linha_cima = determina_linhas_de_guia(
        imagem_original, imagem_pb
    )

    # acha interseccao entre linha do meio e linha de cima
    intersection = acha_interseccao_entre_linhas(
        funcao_linha_cima, funcao_linha_meio, dim_imagem[1], dim_imagem[0]
    )
    cv2.circle(imagem_original, intersection, 5, (0, 255, 255), 5)

    # determina distancia media entre linhas gabarito
    media = calcula_distancia_media_entre_linha_cima_e_baixo(
        funcao_linha_baixo, funcao_linha_cima, dim_imagem[1]
    )

    # encontra ponto para questões e encontra a alternativa marcada
    alternativas_marcadas = []
    pontos_alternativas = []
    for i in range(90):
        ponto_questao = devolve_posicao_ponto_para_questao(
            i, intersection, media, funcao_linha_cima
        )
        alternativa, ponto_alternativa = devolve_alternativa_marcada(
            ponto_questao, imagem_pb, media
        )
        alternativas_marcadas.append(alternativa)
        pontos_alternativas.append(ponto_alternativa)

    return alternativas_marcadas, pontos_alternativas
