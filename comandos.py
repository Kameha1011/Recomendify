from funciones_grafo import bfs, reconstruir_camino, ciclo_particular_dfs, obtener_grados
import random

'''----------------------------------------------------CAMINO-----------------------------------------------------------------'''

FLECHA = " --> "

def camino_minimo(g, inicio, fin, colores):
    if colores[inicio] == 0 or colores[fin] == 0:
        print("Tanto el origen como el destino deben ser canciones")
        return
    orden, padres = bfs(g, inicio, fin)
    if fin not in orden:
        print("No se encontro recorrido")
        return
    printear_camino(g, reconstruir_camino(padres, inicio, fin))
    
def printear_camino(g, camino):
    for i in range(len(camino) - 1):
        playlist = g.peso_arista(camino[i], camino[i+1])
        nombre_playlist = random.choice(list(playlist.values()))
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

def filtro_mas_importantes(diccionario, colores):
    nuevo = {}
    for clave in diccionario:
        if colores[clave] != 0:
            nuevo[clave] = diccionario[clave]
    return nuevo

def mas_importantes(n, g, colores):
    global page_rank
    if len(page_rank) == 0:
        page_rank = pagerank(g)
        page_rank = filtro_mas_importantes(page_rank, colores)
        page_rank = list(page_rank.items())
        page_rank.sort(key=lambda x: x[1], reverse=True)

    for i in range(n-2):
        print(f" {page_rank[i][0]}", end=";")
    print(f" {page_rank[n-1][0]}")
    

'''---------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------Rango----------------------------------------------------'''

def rango(g,n, inicio, orden=None):
    if not orden:
        orden, _ = bfs(g, inicio)
    cont = 0
    for v in g:
        if v in orden and orden[v] == n:
            cont += 1
    print(cont)
    return orden

'''----------------------------------------------------Ciclos---------------------------------------------------------'''


def ciclo_n_canciones(grafo, n, cancion_origen):
    ciclo = ciclo_particular_dfs(grafo, cancion_origen, n)
    if not ciclo:
        print("No se encontró recorrido")
        return
    printear_ciclo(ciclo)

def printear_ciclo(ciclo):
    for i in range(len(ciclo) - 1):
        print(ciclo[i], end=FLECHA)
    print(ciclo[-1])


'''----------------------------------------------------Page Rank Personalizado----------------------------------------------'''

GRADO = 0
ADYACENTE = 1


def random_walk(g, v, largo_camino, grados, page_rank_pers):
    if largo_camino == 0:
        return
    adyacentes = g.adyacentes(v)
    if len(adyacentes) == 0:
        return
    w = random.choice(list(adyacentes.keys()))
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


def filtro(page_rank, colores, condicion, elemento):
    page_rank_filtrado = {}

    for clave in page_rank:
        if clave == elemento:
            continue
        if colores[clave] == condicion:
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

def recomendados(g, lista_canciones, n_recomendados, colores, condicion):
    grados = obtener_grados(g)
    personalizados = []
    for cancion in lista_canciones:
        pr_pers = obtener_page_rank_personalizado(g, 300, grados, cancion)
        pr_pers = filtro(pr_pers, colores, condicion, cancion)
        personalizados.append(pr_pers)
    
    promedio(personalizados, len(personalizados))
    pr_promedio = pr_promediado(personalizados)
    pr_promedio = list(pr_promedio.items())
    pr_promedio.sort(key=lambda x: x[PESO], reverse=True)

    for i in range(n_recomendados - 2):
        print(f"{pr_promedio[i][VERTICE]}", end=" ; ")
    print(pr_promedio[n_recomendados - 1][VERTICE])

'''---------------------------------------------------------------------------------------------------'''