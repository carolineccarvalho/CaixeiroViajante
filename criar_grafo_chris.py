from igraph import *
import numpy as np
import networkx as nx

def criar_grafo2(coordenadas, n, chunk_size=1000):
    g = nx.Graph()
    pontos = np.array([[coord[1], coord[2]] for coord in coordenadas])

    for i, (label, x, y) in enumerate(coordenadas):
        g.add_node(i, label= str(label), x=x, y=y)
    
    for start in range(0,n, chunk_size):
        end = min(start+chunk_size, n)
        dx = pontos[start:end, 0][:, np.newaxis] - pontos[:, 0]
        dy = pontos[start:end, 1][:, np.newaxis] - pontos[:, 1]
        distancias = np.sqrt(dx**2 + dy**2)

        # Criar arestas para o chunk
        for i in range(end - start):
            for j in range(n):
                if i + start < j:  # Apenas parte superior da matriz
                    peso = round(distancias[i, j])
                    g.add_edge(i + start, j, weight=peso)

    return g