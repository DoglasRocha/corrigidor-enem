import os
import csv


def abre_gabaritos(path_gabaritos) -> list:
    gabaritos = []
    for gabarito_path in os.listdir(path_gabaritos):
        with open(f"{path_gabaritos}/{gabarito_path}", newline="") as gabarito:
            gabaritos.append(list(csv.DictReader(gabarito)))

    return gabaritos


def corrige_prova(alternativas_encontradas: list, gabaritos: list) -> list:
    resultado = []

    for n_alternativa in range(len(alternativas_encontradas)):
        correcao_alternativa = []
        for gabarito in gabaritos:
            dict_gabarito = {
                "Matéria": gabarito[n_alternativa]["Matéria"],
                "Correção": "C"
                if alternativas_encontradas[n_alternativa]
                == gabarito[n_alternativa]["Resposta"].lower()
                else "E",
            }
            correcao_alternativa.append(dict_gabarito)

        resultado.append(correcao_alternativa)

    return limpa_resultado(resultado)


def limpa_resultado(resultado: list) -> list:
    for n_resultado in range(len(resultado)):
        for n_materia in range(len(resultado[n_resultado]) - 1):
            if (
                resultado[n_resultado][n_materia]
                != resultado[n_resultado][n_materia + 1]
            ):
                break
        else:
            resultado[n_resultado] = [resultado[n_resultado][0]]

    return resultado
