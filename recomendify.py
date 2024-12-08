#!/usr/bin/python3

from grafo import *
import comandos
import sys
from auxiliares import *
from funciones_grafo import *


def main():
    grafo_proyeccion = None
    # archivo = open(sys.argv[1], "r")
    archivo = open("spotify-mini.tsv", "r")
    grafo_bipartito = construir_grafo_bipartito(archivo)
    archivo.close()
    comandos.recomendados(grafo_bipartito)
    for linea in sys.stdin:
        primer_espacio = linea.find(" ")
        comando = linea[:primer_espacio]
        if comando == "camino":
            cancion_inicio, cancion_fin = linea[primer_espacio:].split(" >>>> ")
            comandos.camino_minimo(grafo_bipartito, cancion_inicio, cancion_fin)
        elif comando == "mas_importantes":
            comandos.mas_importantes(int(parametros), grafo_bipartito)
        elif comando == "recomendacion":
            tipo_vertice = CANCION if parametros[0] == "canciones" else USUARIO
            n = int(parametros[1])
            parametros = " ".join(parametros[2:])
            lista_canciones = parametros.split(" >>>> ")
            comandos.recomendados(grafo_bipartito, lista_canciones, n, tipo_vertice)
        elif comando == "ciclo":
            if not grafo_proyeccion:
                grafo_proyeccion = obtener_grafo_proyeccion(grafo_bipartito)
            n = int(parametros[0])
            parametros = " ".join(parametros[1:])
            comandos.ciclo_n_canciones(grafo_proyeccion, n, parametros)
        elif comando == "rango":
            if not grafo_proyeccion:
                grafo_proyeccion = obtener_grafo_proyeccion(grafo_bipartito)
            n = int(parametros[0])
            parametros = " ".join(parametros[1:])
            comandos.rango(grafo_proyeccion, n, parametros)

main()