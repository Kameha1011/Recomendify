from collections import deque
from grafo import *

def bfs(g:  Grafo, inicio, destino=None, corte= None):
    padres = {inicio : None}
    orden = {inicio: 0}
    visitados = set()
    cola = deque()
    visitados.add(inicio)
    cola.append(inicio)
    
    while len(cola) != 0:
        v = cola.popleft()
        if v == destino:
            return orden, padres
        for w in g.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                padres[w] = v
                orden[w] = orden[v] + 1
                if corte and orden[w] > corte:
                    continue
                cola.append(w)
    return orden, padres

def reconstruir_camino(padres, inicio, fin):
    camino = []
    actual = fin
    while actual != inicio:
        camino.append(actual)
        actual = padres[actual]
    
    camino.append(inicio)
    camino.reverse()
    return camino

def obtener_grados(g : Grafo):
    grados = {}
    for v in g:
        grados[v] = len(g.adyacentes(v))
    return grados

def encontrar_ciclo_largo_n(g : Grafo, inicio, n):
    '''Devuelve un ciclo de largo n que comienza y termina en el vertice inicio, si no existe devuelve None'''
    visitados = set()
    padres = {inicio : None}
    ciclo = _encontrar_ciclo_wrapper(g, inicio, inicio, visitados, padres, 1, n)
    if not ciclo:
        return None
    ciclo.append(inicio)
    return ciclo

def _encontrar_ciclo_wrapper(grafo,v,vertice_origen, visitados, padres, longitud_ciclo, n):
    visitados.add(v)
    if longitud_ciclo > n:
        return None
    for w in grafo.adyacentes(v):
        if w != padres[v] and w == vertice_origen and longitud_ciclo == n:
            return reconstruir_camino(padres, w, v)
        elif w not in visitados:
            padres[w] = v
            ciclo = _encontrar_ciclo_wrapper(grafo, w, vertice_origen, visitados, padres, longitud_ciclo+1, n)
            if ciclo:
                return ciclo
    visitados.remove(v)
    return None

def separar_conjuntos(g):
    conjuntos = {}
    for v in g:
        conjuntos[v.nombre()] = v.tipo
    return conjuntos