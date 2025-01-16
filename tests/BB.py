import math
import time
import argparse
import tracemalloc
import csv
import sys
sys.setrecursionlimit(500000)

coordinates = {
}

adj = []
visited = []
result = math.inf
minors = []
start_time = None

class TimeoutException(Exception):
    pass

    

def parse_tsp_file(file_path):
    dimension = 0
    coordinates = {}
    in_node_coord_section = False

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith("DIMENSION"):
                _, value = line.split()
                dimension = int(value)

            elif line == "NODE_COORD_SECTION":
                in_node_coord_section = True
                continue

            elif in_node_coord_section:
                if line == "EOF":
                    break
                
                
                parts = line.split()
                vertex = int(parts[0]) - 1  
                x, y = map(float, parts[1:])
                coordinates[vertex] = (x, y)

    return dimension, coordinates


def count(element: int, way: list):
    for w in way:
        if w == element:
            return True
    
    return False

def find(element: int, way: list):
    for i in range(len(way)):
        if way[i] == element:
            return i
    
    return -1
            

def findMinor(node:int, n:int):
    Minor = math.inf
    secondMinor = math.inf
    for w in range(n):
        if(w!=node):
            dist = adj[w][node]
            if(dist < Minor):
                aux = Minor
                Minor = dist
                if(aux < secondMinor):
                    secondMinor = aux
            elif(dist < secondMinor):
                secondMinor = dist
    return(Minor, secondMinor)    

def complete(n):
    for i in range(n):
        minors.append(findMinor(i,n))

def distance(node:int,w:int):
    xnode, ynode = coordinates[node]
    xw, yw = coordinates[w]
    return math.trunc((((xnode-xw)**2 + (ynode-yw)**2)**0.5) + 0.5)

def build(m):
    for i in range(m):
        aux = []
        for j in range(m):
            aux.append(distance(i,j))
        adj.append(aux)
    

def recursionBB(estimated:int, weight:int, height:int, N: int, last:int):
    global result, start_time
    
    if time.time() - start_time > 1800:
        print("Tempo limite de 30 minutos atingido. Interrompendo a execução.")
        with open("resultados.csv", "a", newline="") as csvfile:
            campos = ["Arquivo", "Dimensão", "Valor Ótimo", "Tempo de Execução (s)", "Memória Atual (MB)", "Pico de Memória (MB)"]
            escritor = csv.DictWriter(csvfile, fieldnames=campos)
            
            if csvfile.tell() == 0:
                escritor.writeheader()

            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            execution_time = time.time() - start_time
            
            escritor.writerow({
                "Arquivo": file_path,
                "Dimensão": N,
                "Valor Ótimo": "NA",
                "Tempo de Execução (s)": execution_time,
                "Memória Atual (MB)": current / 10**6,
                "Pico de Memória (MB)": peak / 10**6
            })

        sys.exit(0)

    
    if height == N-1:
        if weight + adj[last][0] < result:
            result = weight + adj[last][0]
        return 
        
    for i in range(N):
        if not visited[i]:
            temp = estimated
            new_weight = weight
            
            new_weight += adj[last][i]
            
            minor, secondMinor = minors[i]
            
            minorLast, secondMinorLast = minors[last]
            
            temp -= (((minorLast + minor) / 2) if height == 1 
                            else ((secondMinorLast + minor) / 2)
                        )
            temp = math.ceil(temp)
            temp += adj[last][i]
                
        
            if temp < result:
                visited[i] = True
                recursionBB(temp, new_weight, 
                       height + 1, N, i)
                visited[i] = False
 
            
            
def initialize(N):
    global visited
    build(N)
    complete(N)
    visited = [False]* N
    visited[0] = [True]
    
    
def run(N):  
    global result, start_time 
    start_time = time.time() 
    print("Está executando. Aguarde. :)")
    print()
    tracemalloc.start()
    initialize(N)
    bound = 0
    for i in range(N):
        bound+=minors[i][0]+minors[i][1]
    
    recursionBB(math.ceil(bound / 2), 0, 0, N, 0)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory() 
    tracemalloc.stop()
    execution_time = end_time - start_time
    return result, execution_time, current / 10**6, peak / 10**6


print()
print("##################################")
print("Branch and Bound")
print("##################################")
print()
parser = argparse.ArgumentParser(description="TSP Solver")
parser.add_argument('file_path', type=str, help="Caminho do arquivo TSP")

args = parser.parse_args()
file_path = args.file_path


dimension, coordinates = parse_tsp_file(file_path)  
optimal_value, exec_time, current_mem, peak_mem = run(dimension)
print("Valor ótimo encontrado: ", optimal_value)
print()

with open("resultados.csv", "a", newline="") as csvfile:
    campos = ["Arquivo", "Dimensão", "Valor Ótimo", "Tempo de Execução (s)", "Memória Atual (MB)", "Pico de Memória (MB)"]
    escritor = csv.DictWriter(csvfile, fieldnames=campos)
    
    if csvfile.tell() == 0:
        escritor.writeheader()
    
    
    escritor.writerow({
        "Arquivo": file_path,
        "Dimensão": dimension,
        "Valor Ótimo": optimal_value,
        "Tempo de Execução (s)": exec_time,
        "Memória Atual (MB)": current_mem,
        "Pico de Memória (MB)": peak_mem
    })