#!/usr/bin/python3

from grafo import *
import comandos
import sys

ID_USUARIO = 1
NOMBRE_CANCION = 2
NOMBRE_ARTISTA = 3
ID_PLAYLIST = 4
NOMBRE_PLAYLIST = 5
GENEROS = 6
SEPARADOR = " - "
USUARIO = 0
CANCION = 1

def parsear_linea(linea : str):
    datos = linea.rstrip("\n").split("\t")
    generos = datos[GENEROS].split(",")
    datos[GENEROS] = generos
    return datos

def actualizar_grafo_1(g : Grafo, datos, colores):
    id_usuario = datos[ID_USUARIO]
    cancion = datos[NOMBRE_CANCION] + SEPARADOR + datos[NOMBRE_ARTISTA]
    colores[cancion] = CANCION
    id_playlist = datos[ID_PLAYLIST]
    nombre_playlist = datos[NOMBRE_PLAYLIST]
    colores[id_usuario] = USUARIO
    if cancion not in g:
        g.agregar_vertice(cancion)
    if id_usuario not in g: 
        g.agregar_vertice(id_usuario)
    
    if not g.estan_unidos(id_usuario, cancion): # O(1)
        uniones = {}
        uniones[id_playlist] = nombre_playlist
        g.agregar_arista(id_usuario, cancion, uniones) # O(1)
    else:
        uniones = g.peso_arista(id_usuario, cancion)
        uniones[id_playlist] = nombre_playlist

def construir_grafo_1(archivo):
    colores = {}
    g = Grafo(dirigido=False)
    _ = archivo.readline()
    linea = archivo.readline()
    while linea:
        datos = parsear_linea(linea)
        actualizar_grafo_1(g, datos, colores)
        linea = archivo.readline()
    return g, colores



def obtener_grafo_proyeccion(g, colores):
    grafo_proyeccion = Grafo(False)
    for v in g: 
        if colores[v] != 1:
            adyacentes = list(g.adyacentes(v).keys())
            for i in range (len(adyacentes) - 1):
                grafo_proyeccion.agregar_vertice(adyacentes[i])
                for j in range(i+1, len(adyacentes)):
                    grafo_proyeccion.agregar_vertice(adyacentes[j])
                    grafo_proyeccion.agregar_arista(adyacentes[i], adyacentes[j])
    return grafo_proyeccion



def main():
    grafo_proyeccion = None
    archivo = open(sys.argv[1], "r")
    grafo_bipartito, colores = construir_grafo_1(archivo)
    archivo.close()

    for linea in sys.stdin:
        linea = linea.split()
        comando = linea[0]
        parametros = linea[1:]
        if comando == "camino":
            parametros = " ".join(parametros)
            parametros = parametros.split(" >>>> ")
            comandos.camino_minimo(grafo_bipartito, parametros[0], parametros[1], colores)
        elif comando == "mas_importantes":
            comandos.mas_importantes(int(parametros[0]), grafo_bipartito, colores)
        elif comando == "recomendacion":
            condicion = CANCION if parametros[0] == "canciones" else USUARIO
            n = int(parametros[1])
            parametros = " ".join(parametros[2:])
            lista_canciones = parametros.split(" >>>> ")
            comandos.recomendados(grafo_bipartito, lista_canciones, n, colores, condicion)
        elif comando == "ciclo":
            if not grafo_proyeccion:
                grafo_proyeccion = obtener_grafo_proyeccion(grafo_bipartito, colores)
            n = int(parametros[0])
            parametros = " ".join(parametros[1:])
            comandos.ciclo_n_canciones(grafo_proyeccion, n, parametros)
        elif comando == "rango":
            if not grafo_proyeccion:
                grafo_proyeccion = obtener_grafo_proyeccion(grafo_bipartito, colores)
            n = int(parametros[0])
            parametros = " ".join(parametros[1:])
            comandos.rango(grafo_proyeccion, n, parametros)



main()