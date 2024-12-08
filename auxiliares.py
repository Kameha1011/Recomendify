from grafo import *
from modelos import *

ID_USUARIO = 1
NOMBRE_CANCION = 2
NOMBRE_ARTISTA = 3
ID_PLAYLIST = 4
NOMBRE_PLAYLIST = 5
GENEROS = 6
SEPARADOR = " - "

def parsear_linea(linea : str):
    datos = linea.rstrip("\n").split("\t")
    generos = datos[GENEROS].split(",")
    datos[GENEROS] = generos
    return datos

def actualizar_grafo_bipartito(g : Grafo, datos):
    vertice_usuario = Usuario(datos[ID_USUARIO])
    vertice_cancion = Cancion(datos[NOMBRE_CANCION], datos[NOMBRE_ARTISTA])

    if vertice_usuario not in g:
        g.agregar_vertice(vertice_usuario)
    if vertice_cancion not in g:
        g.agregar_vertice(vertice_cancion)

    if not g.estan_unidos(vertice_cancion, vertice_usuario):
        playlist = Playlist_Usuario()
        playlist.agregar_playlist(datos[NOMBRE_PLAYLIST], datos[ID_PLAYLIST])
        g.agregar_arista(vertice_cancion, vertice_usuario, playlist)
    else:
        playlist_actual = g.peso_arista(vertice_cancion, vertice_usuario)
        playlist_actual.agregar_playlist(datos[NOMBRE_PLAYLIST], datos[ID_PLAYLIST])

def construir_grafo_bipartito(archivo):
    g = Grafo(dirigido=False)
    archivo.readline() # Skip nombres de columnas
    linea = archivo.readline()
    while linea:
        datos = parsear_linea(linea)
        actualizar_grafo_bipartito(g, datos)
        linea = archivo.readline()
    return g

def obtener_grafo_proyeccion(g):
    grafo_proyeccion = Grafo(False)
    for v in g:
        if v.tipo == USUARIO:
            canciones = list(g.adyacentes(v))
            for i in range(len(canciones) - 1):
                grafo_proyeccion.agregar_vertice(canciones[i])
                for j in range(i+1, len(canciones)):
                    grafo_proyeccion.agregar_vertice(canciones[j])
                    grafo_proyeccion.agregar_arista(canciones[i], canciones[j])
    return grafo_proyeccion

