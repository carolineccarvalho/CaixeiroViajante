import subprocess
from tatt import *
from igraph import *
import numpy as np
from chris import *
from tratar_dados import *
from criar_grafo_tatt import *
from criar_grafo_chris import * 
from funcao_lim_tempo import *
from BB import *


def main():
    coordinates = {}
    adj = []
    visited = []
    result = math.inf
    minors = []
    start_time = None
    filename = input("Insira o nome do arquivo TSP (exemplo: bier127.tsp): ").strip()
    try: 
        name, dimension, coordenadas = extrair_dados(filename)

        print(f"Processando {name} com {dimension} cidades...")
        
        print("Escolha o algoritmo para resolver o problema TSP:")
        print("1. Twice-Around-the-Tree (Árvore de Dois Caminhos)")
        print("2. Branch-and-Bound")
        print("3. Christofides")

        algoritmo_escolhido = input("Digite o número correspondente ao algoritmo (1, 2 ou 3): ").strip()

        algoritmos = {
            "1": ("Twice-Around-the-Tree", criar_grafo, tatt),
            "2": ("Branch-and-Bound", None, None),
            "3": ("Christofides", criar_grafo2, chris)
        }

        if algoritmo_escolhido in algoritmos:
            nome_algoritmo, criar_grafo_func, algoritmo = algoritmos[algoritmo_escolhido]

            if algoritmo_escolhido == "2":
                print(f"Executando o algoritmo {nome_algoritmo} no arquivo '{filename}'...")
                try:
                    subprocess.run(["python3", "BB.py", filename], check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    print(f"Erro ao executar o script BB.py:\n{e.stderr}")

            else:
                print(f"Executando o algoritmo {nome_algoritmo}...")
                
                g = criar_grafo_func(coordenadas, dimension)
                resultado = limite_de_tempo(algoritmo, args=(g,), timeout=1800)

                print(f"Resultado: {resultado}")
        else:
            print("Erro: Algoritmo inválido. Por favor, escolha 1, 2 ou 3.")
            return

    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontradoo.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        import traceback
        traceback.print_exc() 


if __name__ == "__main__":
    main()
