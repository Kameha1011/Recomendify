#!/usr/bin/python3

import comandos
import sys
from auxiliares import construir_grafo_bipartito, obtener_grafo_proyeccion

CANCION = 1
USUARIO = 0

CAMINO = "camino"
MAS_IMPORTANTES = "mas_importantes"
RECOMENDACION = "recomendacion"
CICLO = "ciclo"
RANGO = "rango"
SEPARADOR = " >>>> "

ESPACIO = " "
CANCIONES = "canciones"

CANCION = "Cancion"
USUARIO = "Usuario"


def main():
    grafo_proyeccion = None
    archivo = open(sys.argv[1], "r")
    grafo_bipartito, conjuntos = construir_grafo_bipartito(archivo)
    archivo.close()

    for linea in sys.stdin:
        linea = linea.rstrip("\n")
        primer_espacio = linea.find(ESPACIO)
        comando = linea[:primer_espacio]
        linea = linea[primer_espacio+1:]

        if comando == CANCION:
            cancion_inicio, cancion_fin = linea.split(SEPARADOR)
            comandos.camino_minimo(grafo_bipartito, cancion_inicio, cancion_fin, conjuntos)

        elif comando == MAS_IMPORTANTES:
            parametros = linea
            comandos.mas_importantes(int(parametros), grafo_bipartito, conjuntos)

        elif comando == RECOMENDACION:
            espacio = linea.find(ESPACIO)
            tipo = linea[:espacio]
            linea = linea[espacio+1:]
            tipo_vertice = CANCION if tipo == CANCIONES else USUARIO

            espacio = linea.find(ESPACIO)
            n = int(linea[:espacio])
            parametros = linea[espacio+1:]

            lista_canciones = parametros.split(SEPARADOR)
            comandos.recomendados(grafo_bipartito, lista_canciones, n, tipo_vertice, conjuntos)

        elif comando == CICLO:
            if not grafo_proyeccion: grafo_proyeccion = obtener_grafo_proyeccion(grafo_bipartito, conjuntos)
            espacio = linea.find(ESPACIO)
            n = int(linea[:espacio])
            parametros = linea[espacio+1:]
            comandos.ciclo_n_canciones(grafo_proyeccion, n, parametros)

        elif comando == RANGO:
            if not grafo_proyeccion: grafo_proyeccion = obtener_grafo_proyeccion(grafo_bipartito, conjuntos)
            espacio = linea.find(ESPACIO)
            n = int(linea[:espacio])
            parametros = linea[espacio+1:]
            comandos.rango(grafo_proyeccion, n, parametros)

main()