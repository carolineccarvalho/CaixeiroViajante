from igraph import *
import numpy as np

def criar_grafo(coordenadas, n, chunk_size=1000):
    g = Graph()
    g.add_vertices(n)

    pontos = np.array([[coord[1], coord[2]] for coord in coordenadas])

    g.vs["label"] = [str(coord[0]) for coord in coordenadas]
    g.vs["x"] = pontos[:, 0]
    g.vs["y"] = pontos[:, 1]

    for start in range(0, n, chunk_size):
        end = min(start + chunk_size, n)

        dx = pontos[start:end, 0][:, np.newaxis] - pontos[:, 0]
        dy = pontos[start:end, 1][:, np.newaxis] - pontos[:, 1]
        distancias = np.sqrt(dx**2 + dy**2)

        arestas = []
        pesos = []
        for i in range(end - start):
            for j in range(n):
                if i + start < j:  # Apenas parte superior da matriz
                    arestas.append((i + start, j))
                    pesos.append(round(distancias[i, j]))

        # Adicionar as arestas e pesos ao grafo
        g.add_edges(arestas)
        g.es[-len(arestas):]["weight"] = pesos

    return g
