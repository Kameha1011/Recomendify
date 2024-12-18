from funciones_grafo import bfs, reconstruir_camino, encontrar_ciclo_largo_n, obtener_grados
import random
from auxiliares import printer, top_k_recomendaciones, parsear_linea_ciclo_rango, parsear_linea_recomendacion

SEPARADOR_ELEMENTOS = ";"
CANCION = 1
SEPARADOR_CANCIONES = " >>>> "
ESPACIO = " "
NO_CAMINO = "No se encontro recorrido"
FLECHA = " -->"


'''----------------------------------------------------CAMINO-----------------------------------------------------------------'''

NO_SON_CANCIONES = "Tanto el origen como el destino deben ser canciones"
APARECE = "aparece en playlist"
DE = "de"
TIENE = "tiene una playlist"
DONDE = "donde aparece"

def camino_minimo(g, conjuntos, linea):
    inicio, fin = linea.split(SEPARADOR_CANCIONES)
    camino_minimo_wrapped(g, inicio, fin, conjuntos)

def camino_minimo_wrapped(g, inicio, fin, conjuntos):
    if conjuntos[inicio] != CANCION or conjuntos[fin] != CANCION:
        print(NO_SON_CANCIONES)
        return

    orden, padres = bfs(g, inicio, fin)
    if fin not in orden:
        print(NO_CAMINO)
        return
    printear_camino(g, reconstruir_camino(padres, inicio, fin))
    
def printear_camino(g, camino):
    sep = FLECHA + ESPACIO
    for i in range(len(camino) - 1):
        playlists = g.peso_arista(camino[i], camino[i+1])
        nombre_playlist = random.choice(list(playlists.values()))
        if i % 2 == 0:
            print(f"{camino[i]}{sep}{APARECE}{sep}{nombre_playlist}{sep}{DE}{sep}{camino[i+1]}{sep}{TIENE}", end=sep)
        else:
            print(f"{nombre_playlist}{sep}{DONDE}", end=sep)
    
    print(camino[-1])

'''------------------------------------------------Mas Importantes----------------------------------------------------'''

PAGE_RANK = {}
CANTIDAD_ITERACIONES = 100
FACTOR_AMORTIGUACION = 0.85

def pagerank(g, iteraciones = CANTIDAD_ITERACIONES, d=FACTOR_AMORTIGUACION):
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

def filtro_mas_importantes(diccionario, conjuntos):
    nuevo = {}
    for clave in diccionario:
        if conjuntos[clave] == CANCION:
            nuevo[clave] = diccionario[clave]
    return nuevo

def mas_importantes_wrapped(n, g, conjuntos):
    global PAGE_RANK
    if len(PAGE_RANK) == 0:
        PAGE_RANK = pagerank(g)
        PAGE_RANK = filtro_mas_importantes(PAGE_RANK, conjuntos)
        PAGE_RANK = list(PAGE_RANK.items())
        PAGE_RANK.sort(key=lambda x: x[1], reverse=True)

    canciones_mas_importantes = [cancion for cancion, _ in PAGE_RANK[:n+1]]

    printer(canciones_mas_importantes, SEPARADOR_ELEMENTOS)

def mas_importantes(g, conjuntos, linea):
    n = int(linea)
    mas_importantes_wrapped(n, g, conjuntos)

'''----------------------------------------------------Rango----------------------------------------------------'''
def rango_wrapped(g,n, inicio):
    orden, _ = bfs(g, inicio, corte=n)
    cont = 0
    for v in orden:
        if orden[v] == n:
            cont += 1
    print(cont)

def rango(g, linea):
    n, parametros = parsear_linea_ciclo_rango(linea)
    rango_wrapped(g, n, parametros)

'''----------------------------------------------------Ciclos---------------------------------------------------------'''

def ciclo_n_canciones_wrapped(grafo, n, cancion_origen):
    ciclo = encontrar_ciclo_largo_n(grafo, cancion_origen, n)
    if not ciclo:
        print(NO_CAMINO)
        return
    printer(ciclo, FLECHA)

def ciclo_n_canciones(g, linea):
    n, parametros = parsear_linea_ciclo_rango(linea)
    ciclo_n_canciones_wrapped(g, n, parametros)

'''----------------------------------------------------Page Rank Personalizado----------------------------------------------'''

VERTICE = 0
PESO = 1
VALOR_INICIAL_PAGE_RANK = 1
LARGO_CAMINO = 300

def random_walk(g, v, largo_camino, grados, page_rank_pers):
    if largo_camino == 0:
        return
    adyacentes = g.adyacentes(v)
    cant_adyacentes = len(adyacentes)
    if cant_adyacentes == 0:
        return
    w = random.choice(list(adyacentes.keys()))
    if w in page_rank_pers:
        page_rank_pers[w] += (page_rank_pers[v]/grados[v])
    else:
        page_rank_pers[w] = (page_rank_pers[v]/grados[v])
    random_walk(g, w, largo_camino - 1, grados, page_rank_pers)

def obtener_page_rank_personalizado_cancion(g, largo_camino, grados, inicio):
    page_rank_personalizado = {inicio : VALOR_INICIAL_PAGE_RANK}

    for _ in range(CANTIDAD_ITERACIONES):
        random_walk(g, inicio, largo_camino, grados, page_rank_personalizado)
    

    for v in page_rank_personalizado:
        page_rank_personalizado[v] /= CANTIDAD_ITERACIONES

    return page_rank_personalizado


def filtrar_page_rank_personalizado(page_rank, condicion, elemento, conjuntos):
    page_rank_filtrado = {}

    for clave in page_rank:
        if clave == elemento:
            continue
        if conjuntos[clave] == condicion:
            page_rank_filtrado[clave] = page_rank[clave]

    return page_rank_filtrado

def unificar_page_ranks(page_ranks):
    page_rank_unificado = {}
    for pr in page_ranks:
        for clave in pr:
            if clave in page_rank_unificado:
                page_rank_unificado[clave] += pr[clave]
            else:
                page_rank_unificado[clave] = pr[clave]
    return page_rank_unificado


def promediar_page_rank(page_rank, factor):
    for clave in page_rank:
        page_rank[clave] /= factor

def recomendados_wrapper(g, lista_canciones, n_recomendados, condicion, conjuntos):
    grados = obtener_grados(g)
    page_ranks_personalizados = []
    for cancion in lista_canciones:
        pr_pers = obtener_page_rank_personalizado_cancion(g, LARGO_CAMINO, grados, cancion)
        pr_pers = filtrar_page_rank_personalizado(pr_pers, condicion, cancion, conjuntos)
        page_ranks_personalizados.append(pr_pers)
    
    pr_unificado = unificar_page_ranks(page_ranks_personalizados)
    promediar_page_rank(pr_unificado, len(page_ranks_personalizados))
    
    recomendados = top_k_recomendaciones(list(pr_unificado.items()), n_recomendados)
    printer(recomendados, SEPARADOR_ELEMENTOS)

def recomendados(g, conjuntos, linea):
    tipo_vertice, n, lista_canciones = parsear_linea_recomendacion(linea)
    recomendados_wrapper(g, lista_canciones, n, tipo_vertice, conjuntos)


'''---------------------------------------------------------------------------------------------------'''