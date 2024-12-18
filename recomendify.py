#!/usr/bin/python3

import comandos
import sys
from auxiliares import construir_grafo_bipartito, obtener_grafo_proyeccion, obtener_comando



CAMINO = "camino"
MAS_IMPORTANTES = "mas_importantes"
RECOMENDACION = "recomendacion"
CICLO = "ciclo"
RANGO = "rango"

COMANDOS = {
    CAMINO: comandos.camino_minimo,
    MAS_IMPORTANTES: comandos.mas_importantes,
    RECOMENDACION: comandos.recomendados,
    CICLO: comandos.ciclo_n_canciones,
    RANGO: comandos.rango }

def main():
    grafo_proyeccion = None
    archivo = open(sys.argv[1], "r")
    grafo_bipartito, conjuntos = construir_grafo_bipartito(archivo)
    archivo.close()

    for linea in sys.stdin:

        comando, linea = obtener_comando(linea)

        if comando == RANGO or comando == CICLO:
            if not grafo_proyeccion: grafo_proyeccion = obtener_grafo_proyeccion(grafo_bipartito, conjuntos)
            COMANDOS[comando](grafo_proyeccion, linea)
        elif comando in COMANDOS:
            COMANDOS[comando](grafo_bipartito, conjuntos, linea)

main()