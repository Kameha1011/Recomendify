from collections import deque
from grafo import *

def bfs(g : Grafo, inicio, destino=None):
    padres = {inicio : None}
    visitados = set()
    visitados.add(inicio)
    orden = {inicio: 0}
    cola = deque()
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



def ciclo_particular_dfs(g : Grafo, inicio, n):
    '''Devuelve un ciclo de largo n que comienza y termina en el vertice inicio, si no existe devuelve None'''
    visitados = set()
    padres = {inicio : None}
    ciclo = _ciclo_particular_dfs(g, inicio, inicio, visitados, padres, 1, n)
    if not ciclo:
        return None
    ciclo.append(inicio)
    return ciclo

def _ciclo_particular_dfs(grafo,v,vertice_origen, visitados, padres, l, n):
    visitados.add(v)
    if l > n:
        return None
    for w in grafo.adyacentes(v):
        if w != padres[v] and w == vertice_origen and l == n:
            return reconstruir_camino(padres, w, v)
        elif w not in visitados:
            padres[w] = v
            ciclo = _ciclo_particular_dfs(grafo, w, vertice_origen, visitados, padres, l+1, n)
            if ciclo:
                return ciclo
    visitados.remove(v)
    return None

