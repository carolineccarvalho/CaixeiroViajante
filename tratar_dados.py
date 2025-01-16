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
