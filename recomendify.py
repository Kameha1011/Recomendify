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

    comandos.camino_minimo(grafo_bipartito, "Don't Go Away - Oasis", "Quitter - Eminem")
    # for linea in sys.stdin:
    #     linea = linea.split()
    #     comando = linea[0]
    #     parametros = linea[1:]
    #     if comando == "camino":
    #         parametros = " ".join(parametros)
    #         parametros = parametros.split(" >>>> ")
    #         comandos.camino_minimo(grafo_bipartito, parametros[0], parametros[1], colores)
    #     elif comando == "mas_importantes":
    #         comandos.mas_importantes(int(parametros[0]), grafo_bipartito, colores)
    #     elif comando == "recomendacion":
    #         condicion = CANCION if parametros[0] == "canciones" else USUARIO
    #         n = int(parametros[1])
    #         parametros = " ".join(parametros[2:])
    #         lista_canciones = parametros.split(" >>>> ")
    #         comandos.recomendados(grafo_bipartito, lista_canciones, n, colores, condicion)
    #     elif comando == "ciclo":
    #         if not grafo_proyeccion:
    #             grafo_proyeccion = obtener_grafo_proyeccion(grafo_bipartito, colores)
    #         n = int(parametros[0])
    #         parametros = " ".join(parametros[1:])
    #         comandos.ciclo_n_canciones(grafo_proyeccion, n, parametros)
    #     elif comando == "rango":
    #         if not grafo_proyeccion:
    #             grafo_proyeccion = obtener_grafo_proyeccion(grafo_bipartito, colores)
    #         n = int(parametros[0])
    #         parametros = " ".join(parametros[1:])
    #         comandos.rango(grafo_proyeccion, n, parametros)

main()