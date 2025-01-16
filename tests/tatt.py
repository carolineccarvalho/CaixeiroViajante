import pandas as pd
from igraph import *
import math

def prim_algorithm(g):
    peso_total = 0
    num_vertices = g.vcount()
    selecionados = [False] * num_vertices
    arestas_p_min = [float("inf")] * num_vertices
    arestas_p_min[0] = 0
    f = Graph()
    f.add_vertices(num_vertices)
    pai = [-1] * num_vertices

    for i in range(num_vertices):
        v = -1
        for j in range(num_vertices):
            if (selecionados[j] == False) and (v == -1 or arestas_p_min[j] < arestas_p_min[v]):
                v = j
                
        if(arestas_p_min[v] == float("inf")):
            print("Grafo desconexo\n")
            exit(0)

        selecionados[v] = True
        peso_total += arestas_p_min[v]

        for k in range(num_vertices):
            peso = g[v, k]
            if peso != 0 and peso < arestas_p_min[k] and selecionados[k] == False:
                arestas_p_min[k] = peso
                pai[k] = v 
    # print("Arestas da MST:")
    for i in range(1, num_vertices):
        f.add_edge(pai[i], i, weight = g[pai[i], i])
        f.add_edge(i, pai[i], weight = g[pai[i], i])
    return f

def dfs(f, v, visitados, caminho):
    visitados[v] = True
    caminho.append(v)
    for u in f.neighbors(v):
        if not visitados[u]:
            dfs(f, u, visitados, caminho)
            caminho.append(v)

def hamiltoniano(caminho, g):
    caminho_hamiltoniano = []
    visitados = set()
    custo_total = 0
    for i in range(len(caminho) - 1):
        u = caminho[i]
        v = caminho[i + 1]
        if u not in visitados:
            caminho_hamiltoniano.append(u)
            visitados.add(u)
        eid = g.get_eid(u, v)
        custo_total += g.es[eid]["weight"]

    caminho_hamiltoniano.append(caminho[0])
    return caminho_hamiltoniano, custo_total

def tatt(g):
    f = prim_algorithm(g)
    n_vertices = f.vcount()
    caminho = []
    visitados = [False] * n_vertices
    dfs(f, 0, visitados, caminho)
    caminho_hamiltoniano, custo_total = hamiltoniano(caminho, g)
    return caminho_hamiltoniano, custo_total