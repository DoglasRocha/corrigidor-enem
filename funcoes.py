import cv2
from typing import Callable

def faz_funcao_da_reta_para_x(pos_linhas: list, pos_colunas: list) -> Callable:
    m = (pos_linhas[0] - pos_linhas[1]) / (pos_colunas[0] - pos_colunas[1])
    
    return lambda x: int(round(m * x - m * pos_colunas[0] + pos_linhas[0]))

def faz_funcao_da_reta_para_y(pos_linhas: list, pos_colunas: list) -> Callable:
    if (pos_colunas[0] - pos_colunas[1] == 0):
        return lambda y: pos_colunas[0]
    
    m = (pos_linhas[0] - pos_linhas[1]) / (pos_colunas[0] - pos_colunas[1])
    
    return lambda y: int(round((y +  m * pos_colunas[0] - pos_linhas[0]) / m))

def pega_funcao_linha_de_baixo(imagem_pb: cv2.Mat) -> Callable:
    
    tam_y, tam_x = imagem_pb.shape
    pos_colunas = [
        70, 
        tam_x - 70
    ]
    pos_linhas = [-1, -1]
    
    for i in range(len(pos_colunas)):
        for j in range(tam_y - 25, 0, -1):
            if (imagem_pb[j][pos_colunas[i]] == 0):
                pos_linhas[i] = j
                break
    
    return faz_funcao_da_reta_para_x(pos_linhas, pos_colunas)

def pega_funcao_linha_meio(funcao_linha_baixo: Callable, imagem_pb: cv2.Mat) -> Callable:
    tam_y, tam_x = imagem_pb.shape
    pos_colunas_esq = [tam_x // 2 - 100, -1]
    pos_colunas_dir = [tam_x // 2 + 100, -1]

    y1 = funcao_linha_baixo(pos_colunas_esq[0]) - 5
    
    # rotina para encontrar linha do meio
    for i in range(2):    
        for j in range(pos_colunas_esq[0], tam_x):
            if (imagem_pb[y1][j] == 0):
                pos_colunas_esq[i] = j
                y1 = y1 - 300
                break
            
    y2 = funcao_linha_baixo(pos_colunas_dir[0]) - 5
    for i in range(2):    
        for j in range(pos_colunas_dir[0] + 6, 0, -1):
            if (imagem_pb[y2][j] == 0):
                pos_colunas_dir[i] = j
                y2 = y2 - 300
                break 
            
    # colunas da linha do meio serao a media das colunas da direita e da esquerda
    pos_colunas = [(pos_colunas_dir[i] + pos_colunas_esq[i]) / 2 for i in range(2)]
            
    return faz_funcao_da_reta_para_y([(y1 + y2) / 2 + 600, (y1 + y2) / 2 + 300], pos_colunas)

def pega_funcao_linha_cima(funcao_linha_baixo: Callable, funcao_linha_meio: Callable, imagem_pb: cv2.Mat) -> Callable:
    x_meio = imagem_pb.shape[1] // 2 - 100
    y_meio = funcao_linha_baixo(x_meio) - 5
    points_DEBUG = []
    
    # rotina para encontrar linha do meio    
    for j in range(x_meio, imagem_pb.shape[0]):
        if (imagem_pb[y_meio][j] == 0):
            x_meio = j
            break
        
    y_baixo_meio = funcao_linha_baixo(x_meio)
    
    # rotina para acompanhar a linha do meio até sair
    y_quebra = -1
    for i in range(y_baixo_meio, 0, -20):
        points_DEBUG.append((funcao_linha_meio(i), i))
        if (imagem_pb[i][int(funcao_linha_meio(i))] != 0):
            y_quebra = i
            break
        
    # rotina para achar linha de cima
    pos_colunas = [
        imagem_pb.shape[1] // 2 - 200,
        imagem_pb.shape[1] // 2 + 200
    ]
    
    pos_linhas = [
        y_quebra, 
        -1
    ]
        
    for i in range(2):
        for j in range(y_quebra, imagem_pb.shape[0]):
            points_DEBUG.append((pos_colunas[i], j))
            if (imagem_pb[j][pos_colunas[i]] == 0):
                pos_linhas[i] = j
                break
    
    '''for point in points_DEBUG:
        cv2.circle(imagem_pb, point, 5, (0,0,0), 5)'''
    # cv2.imshow("a", imagem_pb[600:])
    # cv2.waitKey(0)
                
    return faz_funcao_da_reta_para_x(pos_linhas, pos_colunas)
    