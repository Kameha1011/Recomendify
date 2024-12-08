from funciones_grafo import bfs, reconstruir_camino, encontrar_ciclo_largo_n, obtener_grados
import random
from modelos import *
from auxiliares import printer, obtener_vertice_cancion

'''----------------------------------------------------CAMINO-----------------------------------------------------------------'''

FLECHA = " --> "

def camino_minimo(g, inicio, fin):
    vertice_inicio = obtener_vertice_cancion(inicio)
    vertice_fin = obtener_vertice_cancion(fin)
    if  not vertice_inicio or not vertice_fin:
        print("Tanto el origen como el destino deben ser canciones")
        return
    orden, padres = bfs(g, vertice_inicio, vertice_fin)
    if vertice_fin not in orden:
        print("No se encontro recorrido")
        return
    printear_camino(g, reconstruir_camino(padres, vertice_inicio, vertice_fin))
    
def printear_camino(g, camino):
    for i in range(len(camino) - 1):
        playlist = g.peso_arista(camino[i], camino[i+1])
        nombre_playlist = playlist[random.randint(0, len(playlist) - 1)].nombre
        if i%2 == 0:
            print(f"{camino[i]}", end=FLECHA)
            print("aparece en playlist", end=FLECHA)
            print(f"{nombre_playlist}", end=FLECHA)
            print("de", end=FLECHA)
            print(f"{camino[i+1]}", end=FLECHA)
            print("tiene una playlist", end=FLECHA)
        else:
            print(f"{nombre_playlist}", end=FLECHA)
            print(f"donde aparece", end=FLECHA)
    
    print(camino[-1])
    
'''---------------------------------------------------------------------------------------------------'''

'''------------------------------------------------Mas Importantes----------------------------------------------------'''

page_rank = {}

def pagerank(g, iteraciones = 100, d=0.85):
    pr = {}
    n = len(g)
    acceso_aleatorio = (1-d) / n

    for v in g:
        pr[v] = 1/n

    for _ in range(iteraciones):
        nuevo_pr = {}
        for v in g:
            sumatoria = 0
            adyacentes = g.adyacentes(v)
            for w in adyacentes:
                sumatoria += pr[w]/len(g.adyacentes(w))
            nuevo_pr[v] = acceso_aleatorio + (d*sumatoria)
        
        pr = nuevo_pr

    return pr

def filtro_mas_importantes(diccionario):
    nuevo = {}
    for clave in diccionario:
        if clave.tipo == CANCION:
            nuevo[clave] = diccionario[clave]
    return nuevo

def mas_importantes(n, g):
    global page_rank
    if len(page_rank) == 0:
        page_rank = pagerank(g)
        page_rank = filtro_mas_importantes(page_rank)
        page_rank = list(page_rank.items())
        page_rank.sort(key=lambda x: x[1], reverse=True)

    canciones_mas_importantes = [cancion for cancion, _ in page_rank[:n]]

    printer(canciones_mas_importantes, " ; ")
    
    
    

'''---------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------Rango----------------------------------------------------'''

def rango(g,n, inicio, orden):
    orden, _ = bfs(g, inicio, corte=n)
    cont = 0
    for v in orden:
        if orden[v] == n:
            cont += 1
    print(cont)

'''----------------------------------------------------Ciclos---------------------------------------------------------'''


def ciclo_n_canciones(grafo, n, cancion_origen):
    ciclo = encontrar_ciclo_largo_n(grafo, cancion_origen, n)
    if not ciclo:
        print("No se encontro recorrido")
        return
    printer(ciclo, FLECHA)


'''----------------------------------------------------Page Rank Personalizado----------------------------------------------'''

GRADO = 0


def random_walk(g, v, largo_camino, grados, page_rank_pers):
    if largo_camino == 0:
        return
    adyacentes = g.adyacentes(v)
    cant_adyacentes = len(adyacentes)
    if cant_adyacentes == 0:
        return
    w = adyacentes[random.randint(0, cant_adyacentes - 1)]
    if w in page_rank_pers:
        page_rank_pers[w] += (page_rank_pers[v]/grados[v])
    else:
        page_rank_pers[w] = (page_rank_pers[v]/grados[v])
    random_walk(g, w, largo_camino - 1, grados, page_rank_pers)

def obtener_page_rank_personalizado(g, largo_camino, grados, inicio):
    page_rank_personalizado = {inicio : 1}

    for _ in range(100):
        random_walk(g, inicio, largo_camino, grados, page_rank_personalizado)
    for v in g:
        if v not in page_rank_personalizado:
            page_rank_personalizado[v] = 0
        else:
            page_rank_personalizado[v] /= 100

    return page_rank_personalizado


PESO = 1
VERTICE = 0


def filtro(page_rank, condicion, elemento):
    page_rank_filtrado = {}

    for clave in page_rank:
        if clave == elemento:
            continue
        if clave.tipo == condicion:
            page_rank_filtrado[clave] = page_rank[clave]

    return page_rank_filtrado

def pr_promediado(prs):
    pr_promedio = {}
    for pr in prs:
        for clave in pr:
            if clave in pr_promedio:
                pr_promedio[clave] += pr[clave]
            else:
                pr_promedio[clave] = pr[clave]
    return pr_promedio


def promedio(page_ranks, k):
    for pr in page_ranks:
        for clave in pr:
            pr[clave] /= k

def recomendados(g, lista_canciones, n_recomendados, condicion):
    grados = obtener_grados(g)
    personalizados = []
    for cancion in lista_canciones:
        pr_pers = obtener_page_rank_personalizado(g, 300, grados, cancion)
        pr_pers = filtro(pr_pers, condicion, cancion)
        personalizados.append(pr_pers)
    
    promedio(personalizados, len(personalizados))
    pr_promedio = pr_promediado(personalizados)
    pr_promedio = list(pr_promedio.items())
    pr_promedio.sort(key=lambda x: x[PESO], reverse=True)

    recomendados = []
    for i in range(n_recomendados):
        recomendados.append(pr_promedio[i][VERTICE])
    
    printer(recomendados, " ; ")


'''---------------------------------------------------------------------------------------------------'''