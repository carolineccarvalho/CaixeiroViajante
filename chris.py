import networkx as nx
import pandas as pd


def chris(g):
    agm = nx.minimum_spanning_tree(g, algorithm="prim")
        
    vertices_impares = []
    for v in agm.nodes:
        if agm.degree[v] % 2 == 1:
            vertices_impares.append(v)
    # print(vertices_impares)

    subgrafo = nx.complete_graph(vertices_impares)
    for u, v in subgrafo.edges:
        subgrafo[u][v]["weight"] = nx.shortest_path_length(g, source=u, target=v, weight="weight")
    
    matching_min = nx.algorithms.matching.min_weight_matching(subgrafo, weight='weight')
    # blz, agora precisamos unir o emparelhamento e a árvore geradora para formar um multigrafo euleriano

    multigrafo = nx.MultiGraph(agm)
    for u, v in matching_min:
        multigrafo.add_edge(u, v, weight = subgrafo[u][v]["weight"])
    
    #vamos encontrar um circuito euleriano
    circuito_euleriano = list(nx.eulerian_circuit(multigrafo))
    #agora o hamiltoniano
    caminho_hamiltoniano = []
    visitados = set()
    custo_total = 0
    for u, v in circuito_euleriano:
        if u not in visitados:
            caminho_hamiltoniano.append(u)
            visitados.add(u)
        custo_total += g[u][v]["weight"] 
    caminho_hamiltoniano.append(caminho_hamiltoniano[0])
    
    return caminho_hamiltoniano