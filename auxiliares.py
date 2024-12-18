import heapq
from grafo import *

ID_USUARIO = 1
NOMBRE_CANCION = 2
NOMBRE_ARTISTA = 3
ID_PLAYLIST = 4
NOMBRE_PLAYLIST = 5
GENEROS = 6
SEPARADOR = " - "
SEPARADOR_ELEMENTOS = ";"
USUARIO = 0
CANCION = 1
ESPACIO = " "
SEPARADOR_CANCIONES = " >>>> "
TABULADOR = "\t"
COMA = ","
FIN_LINEA = "\n"

def parsear_linea(linea : str):
    datos = linea.rstrip(FIN_LINEA).split(TABULADOR)
    generos = datos[GENEROS].split(COMA)
    datos[GENEROS] = generos
    return datos

def actualizar_grafo_bipartito(g : Grafo, datos, conjuntos):
    usuario = datos[ID_USUARIO]
    conjuntos[usuario] = USUARIO
    cancion = f"{datos[NOMBRE_CANCION]}{SEPARADOR}{datos[NOMBRE_ARTISTA]}"
    conjuntos[cancion] = CANCION

    if usuario not in g:
        g.agregar_vertice(usuario)
    if cancion not in g:
        g.agregar_vertice(cancion)

    id_playlist = datos[ID_PLAYLIST]
    nombre_playlist = datos[NOMBRE_PLAYLIST]

    if not g.estan_unidos(usuario, cancion):
        uniones = {}
        uniones[id_playlist] = nombre_playlist
        g.agregar_arista(usuario, cancion, uniones)
    else:
        uniones = g.peso_arista(usuario, cancion)
        uniones[id_playlist] = nombre_playlist

def construir_grafo_bipartito(archivo):
    conjuntos = {}
    g = Grafo(dirigido=False)
    archivo.readline() # Skip nombres de columnas
    linea = archivo.readline()
    while linea:
        datos = parsear_linea(linea)
        actualizar_grafo_bipartito(g, datos, conjuntos)
        linea = archivo.readline()
    return g, conjuntos

def obtener_grafo_proyeccion(g, conjunto):
    grafo_proyeccion = Grafo(False)
    for v in g:
        if conjunto[v] == USUARIO:
            canciones = list(g.adyacentes(v))
            for i in range(len(canciones) - 1):
                grafo_proyeccion.agregar_vertice(canciones[i])
                for j in range(i+1, len(canciones)):
                    grafo_proyeccion.agregar_vertice(canciones[j])
                    grafo_proyeccion.agregar_arista(canciones[i], canciones[j])
    return grafo_proyeccion

def printer(elementos, separador):
    for i in range(len(elementos) - 1):
            print(f" {elementos[i]}", end=separador)
    print(f" {elementos[-1]}")

def top_k_recomendaciones(lista_page_rank, k):
    lista_invertida = []
    for vertice, puntuacion in lista_page_rank:
        lista_invertida.append((-puntuacion, vertice))
    
    heapq.heapify(lista_invertida)
    top_k_valores = []
    for _ in range(k):
        _, vertice = heapq.heappop(lista_invertida)
        top_k_valores.append(vertice)
    return top_k_valores

def parsear_linea_ciclo_rango(linea):
    espacio = linea.find(ESPACIO)
    n = int(linea[:espacio])
    parametros = linea[espacio+1:]
    return n, parametros

def obtener_comando(linea):
    linea = linea.rstrip(FIN_LINEA)
    primer_espacio = linea.find(ESPACIO)
    comando = linea[:primer_espacio]
    linea = linea[primer_espacio+1:]
    return comando, linea

CANCIONES = "canciones"

def parsear_linea_recomendacion(linea):
    espacio = linea.find(ESPACIO)
    tipo = linea[:espacio]
    linea = linea[espacio+1:]
    tipo_vertice = CANCION if tipo == CANCIONES else USUARIO

    espacio = linea.find(ESPACIO)
    n = int(linea[:espacio])
    parametros = linea[espacio+1:]

    lista_canciones = parametros.split(SEPARADOR_CANCIONES)
    return tipo_vertice, n, lista_canciones
