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

def hamiltoniano(caminho, inicio):
    caminho_hamiltoniano = []
    visitados = set()
    for v in caminho:
        if v not in visitados:
            caminho_hamiltoniano.append(v)
            visitados.add(v)
    caminho_hamiltoniano.append(inicio)
    return caminho_hamiltoniano

def tatt(g):
    f = prim_algorithm(g)
    n_vertices = f.vcount()
    caminho = []
    visitados = [False] * n_vertices
    dfs(f, 0, visitados, caminho)
    caminho_hamiltoniano = hamiltoniano(caminho, 0)
    return caminho_hamiltoniano

# def main():
#     g = Graph()
#     g.add_vertices(5)
#     g.add_edges([(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1,4), (2,3), (2,4), (3,4)])
#     g.es["weight"] = [4, 8, 9, 12, 6, 8, 9, 10, 11, 7] 

#     # transforma pesos em matriz de adjacência
#     adj_matrix = [[0] * g.vcount() for _ in range(g.vcount())]
#     for edge in g.es:
#         u, v = edge.tuple
#         adj_matrix[u][v] = adj_matrix[v][u] = edge["weight"]

#     # Converte matriz para igraph e executa Prim
#     g = Graph.Weighted_Adjacency(adj_matrix, mode=ADJ_UNDIRECTED)
#     # algoritmo de Prim
#     f = prim_algorithm(g)
#     print(f)
#     # agora queremos encontrar um caminhe que a partir de um vértice inicial percorra todos ps outros e retorne para o inicial
#     n_vertices = f.vcount()
#     caminho = []
#     visitados = [False] * n_vertices
#     dfs(f, 0, visitados, caminho)
#     print(caminho)

#     caminho_hamiltoniano = hamiltoniano(caminho, 0)
#     print(caminho_hamiltoniano)


# if __name__ == "__main__":
#     main()