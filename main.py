from tatt import *
from igraph import *
from joblib import Parallel, delayed
import math
import numpy as np
import time
import tracemalloc
import threading
import os
import csv

def extrair_dados(arquivo_nome):

    with open(arquivo_nome, "r") as arquivo:
        linhas = arquivo.readlines()

    name = ""
    dimensao = 0
    coordenadas = []

    for line in linhas:
        line = line.strip()
        if line.startswith("NAME"):
            name = line.split(":")[1].strip()
        elif line.startswith("DIMENSION"):
            dimensao = int(line.split(":")[1].strip())
        elif line == "NODE_COORD_SECTION":
            break
        
    node_section_index = linhas.index("NODE_COORD_SECTION\n") + 1
    for i in range(node_section_index, node_section_index+dimensao):
        parts = linhas[i].strip().split()
        coordenadas.append((int(parts[0]), float(parts[1]), float(parts[2])))

    return name, dimensao, coordenadas

def criar_grafo(coordenadas, n, chunk_size=1000):
    g = Graph()
    g.add_vertices(n)

    # Coordenadas como matriz numpy
    pontos = np.array([[coord[1], coord[2]] for coord in coordenadas])

    # Adicionar vértices e propriedades
    g.vs["label"] = [str(coord[0]) for coord in coordenadas]
    g.vs["x"] = pontos[:, 0]
    g.vs["y"] = pontos[:, 1]

    # Adicionar arestas em chunks
    for start in range(0, n, chunk_size):
        end = min(start + chunk_size, n)

        # Cálculo vetorizado das distâncias
        dx = pontos[start:end, 0][:, np.newaxis] - pontos[:, 0]
        dy = pontos[start:end, 1][:, np.newaxis] - pontos[:, 1]
        distancias = np.sqrt(dx**2 + dy**2)

        # Criar arestas para o chunk
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

def limite_de_tempo(g, resultado):
    try:
        resultado["caminho"] = tatt(g)
    except Exception as e:
        resultado["erro"] = str(e)

def main():
    # name, dimensao, coordenadas = extrair_dados("rl5915.tsp")
    # print(f"Processando {name} com {dimensao}")
    # g = criar_grafo(coordenadas, dimensao)
    
    folder = "[0,5000]"
    resultados = []
    for filename in os.listdir(folder):
        if filename.endswith(".tsp"):
            filepath = os.path.join(folder, filename)
            name, dimension, coordenadas = extrair_dados(filepath)
            print(f"Processando {name} com {dimension}")
            g = criar_grafo(coordenadas, dimension)

            tempo_max = 1800
            resultado = {"caminho" : None, "timeout" : False, "erro" : None}

            # Execução sequencial: sem threading
            start_time = time.time()
            tracemalloc.start()
            limite_de_tempo(g, resultado)  # Chamada direta, sem thread
            end_time = time.time()

            espaco_atual, pico_espaco = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            tempo_de_execucao = end_time - start_time

            print(tempo_de_execucao)
            print(f"Memória atual: {espaco_atual / 10**6:.2f} MB")
            print(f"Pico de memória: {pico_espaco / 10**6:.2f} MB")
            
            resultados.append({
                "Arquivo": filename,
                "Nome": name,
                "Dimensão": dimension, 
                "Tempo de Execução (s)": tempo_de_execucao,
                "Memória Atual (MB)": espaco_atual / 10**6,
                "Pico de Memória (MB)": pico_espaco / 10**6,
                "Timeout": resultado["timeout"],
                "Erro": resultado["erro"]
            })

            with open("resultados.csv", "w", newline="") as csvfile:
                campos = ["Arquivo", "Nome", "Dimensão", "Tempo de Execução (s)", "Memória Atual (MB)",
                           "Pico de Memória (MB)", "Timeout", "Erro"]
                escritor = csv.DictWriter(csvfile, fieldnames=campos)
                escritor.writeheader()
                escritor.writerows(resultados)


if __name__ == "__main__":
    main()