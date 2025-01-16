from tatt import *
from igraph import *
import numpy as np
import time
import tracemalloc
import os
import csv
from chris import *
import multiprocessing

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

def limite_de_tempo(func, args=(), timeout=1800):
    # try:
    #     # resultado["caminho"] = tatt(g)
    #     resultado["caminho"] = chris(g)
    # except Exception as e:
    #     resultado["erro"] = str(e)
    resultado = {"caminho": None, "erro": None, "timeout": False}
    def func_wrapper(queue, *args):
        try:
            resultado = func(*args)
            queue.put(resultado)
        except Exception as e:
            queue.put(e)
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=func_wrapper, args=(queue, *args))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        resultado["timeout"] = True
        resultado["erro"] = f"Tempo limite de {timeout}s excedido"
    else:
        process.close()
        if not queue.empty():
            res = queue.get()
            if isinstance(res, Exception):
                resultado["erro"] = str(res)
            else:
                resultado["caminho"] = res
    return resultado

def main():
    resultados = []

    filename = ("rl5934.tsp")
    name, dimension, coordenadas = extrair_dados(filename)
    print(f"Processando {name} com {dimension}")
    g = criar_grafo2(coordenadas, dimension)
    start_time = time.time()
    tracemalloc.start()

    resultado = limite_de_tempo(chris, args=(g,), timeout = 1800)

    end_time = time.time()

    espaco_atual, pico_espaco = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tempo_de_execucao = end_time - start_time

    custo_total = 0
    if resultado["caminho"] and not resultado["erro"]:
        caminho = resultado["caminho"]
        for i in range(len(caminho) - 1):
            u, v = caminho[i], caminho[i + 1]
            custo_total += g[u][v]["weight"] 

    print(tempo_de_execucao)
    print(f"Memória atual: {espaco_atual / 10**6:.2f} MB")
    print(f"Pico de memória: {pico_espaco / 10**6:.2f} MB")
    print(f"Custo ótimo: {custo_total}")
    resultados.append({
        "Arquivo": filename,
        "Nome": name,
        "Dimensão": dimension, 
        "Tempo de Execução (s)": tempo_de_execucao,
        "Memória Atual (MB)": espaco_atual / 10**6,
        "Pico de Memória (MB)": pico_espaco / 10**6,
        "Custo Total": custo_total,
        "Timeout": resultado["timeout"],
        "Erro": resultado["erro"]
    })

    with open("resultados.csv", "a", newline="") as csvfile:
        campos = ["Arquivo", "Nome", "Dimensão", "Tempo de Execução (s)", "Memória Atual (MB)",
                    "Pico de Memória (MB)", "Custo Total", "Timeout", "Erro"]
        escritor = csv.DictWriter(csvfile, fieldnames=campos)
        if csvfile.tell() == 0:
            escritor.writeheader()
        escritor.writerows(resultados)


    # folder = "[0,5000]"
    # resultados = []
    # for filename in os.listdir(folder):
    #     if filename.endswith(".tsp"):
    #         filepath = os.path.join(folder, filename)
    #         name, dimension, coordenadas = extrair_dados(filepath)
    #         print(f"Processando {name} com {dimension}")
    #         g = criar_grafo(coordenadas, dimension)

    #         tempo_max = 1800
    #         resultado = {"caminho" : None, "timeout" : False, "erro" : None}

    #         # Execução sequencial: sem threading
            # start_time = time.time()
            # tracemalloc.start()
            # limite_de_tempo(g, resultado)  # Chamada direta, sem thread
            # end_time = time.time()

            # espaco_atual, pico_espaco = tracemalloc.get_traced_memory()
            # tracemalloc.stop()

            # tempo_de_execucao = end_time - start_time

            # print(tempo_de_execucao)
            # print(f"Memória atual: {espaco_atual / 10**6:.2f} MB")
            # print(f"Pico de memória: {pico_espaco / 10**6:.2f} MB")
            
            # resultados.append({
            #     "Arquivo": filename,
            #     "Nome": name,
            #     "Dimensão": dimension, 
            #     "Tempo de Execução (s)": tempo_de_execucao,
            #     "Memória Atual (MB)": espaco_atual / 10**6,
            #     "Pico de Memória (MB)": pico_espaco / 10**6,
            #     "Timeout": resultado["timeout"],
            #     "Erro": resultado["erro"]
            # })

            # with open("resultados.csv", "w", newline="") as csvfile:
            #     campos = ["Arquivo", "Nome", "Dimensão", "Tempo de Execução (s)", "Memória Atual (MB)",
            #                "Pico de Memória (MB)", "Timeout", "Erro"]
            #     escritor = csv.DictWriter(csvfile, fieldnames=campos)
            #     escritor.writeheader()
            #     escritor.writerows(resultados)

    # folder = "[0,5000]"
    # resultados = []
    # for filename in os.listdir(folder):
    #     if filename.endswith(".tsp"):
    #         filepath = os.path.join(folder, filename)
    #         name, dimension, coordenadas = extrair_dados(filepath)
    #         print(f"Processando {name} com {dimension}")
    #         g = criar_grafo2(coordenadas, dimension)

            # start_time = time.time()
            # tracemalloc.start()

            # resultado = limite_de_tempo(chris, args=(g,), timeout = 60)
    
            # end_time = time.time()

            # espaco_atual, pico_espaco = tracemalloc.get_traced_memory()
            # tracemalloc.stop()

            # tempo_de_execucao = end_time - start_time

            # print(tempo_de_execucao)
            # print(f"Memória atual: {espaco_atual / 10**6:.2f} MB")
            # print(f"Pico de memória: {pico_espaco / 10**6:.2f} MB")
            
            # resultados.append({
            #     "Arquivo": filename,
            #     "Nome": name,
            #     "Dimensão": dimension, 
            #     "Tempo de Execução (s)": tempo_de_execucao,
            #     "Memória Atual (MB)": espaco_atual / 10**6,
            #     "Pico de Memória (MB)": pico_espaco / 10**6,
            #     "Timeout": resultado["timeout"],
            #     "Erro": resultado["erro"]
            # })

            # with open("resultados.csv", "w", newline="") as csvfile:
            #     campos = ["Arquivo", "Nome", "Dimensão", "Tempo de Execução (s)", "Memória Atual (MB)",
            #                "Pico de Memória (MB)", "Timeout", "Erro"]
            #     escritor = csv.DictWriter(csvfile, fieldnames=campos)
            #     escritor.writeheader()
            #     escritor.writerows(resultados)

    

if __name__ == "__main__":
    main()