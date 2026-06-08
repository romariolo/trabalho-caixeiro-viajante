import sys
import math

# ==========================================
# REGISTRO DE USO DE IA (Para o Relatório)
# Prompts utilizados:
# 1. "Crie um parser em Python para ler o formato TSPLIB da entrada padrão (stdin) e uma função para calcular a distância EUC_2D..."
# 2. "Escreva uma função em Python que implemente a heurística do Vizinho Mais Próximo..."
# 3. "Implemente a busca local 2-Opt em Python para otimizar uma rota do TSP..."
# ==========================================

def calcular_distancia(cidade_a, cidade_b):
    """Calcula a distância EUC_2D."""
    xd = cidade_a[1] - cidade_b[1]
    yd = cidade_a[2] - cidade_b[2]
    return math.floor(0.5 + math.sqrt(xd*xd + yd*yd))

def vizinho_mais_proximo(cidades):
    """Constrói uma solução inicial."""
    if not cidades:
        return [], 0

    mapa_cidades = {c[0]: c for c in cidades}
    cidade_atual = cidades[0]
    tour = [cidade_atual[0]]
    nao_visitadas = set([c[0] for c in cidades[1:]])
    custo_total = 0

    while nao_visitadas:
        cidade_mais_proxima = None
        menor_distancia = float('inf')

        for id_candidata in nao_visitadas:
            candidata = mapa_cidades[id_candidata]
            distancia = calcular_distancia(cidade_atual, candidata)
            
            if distancia < menor_distancia:
                menor_distancia = distancia
                cidade_mais_proxima = candidata

        tour.append(cidade_mais_proxima[0])
        custo_total += menor_distancia
        nao_visitadas.remove(cidade_mais_proxima[0])
        cidade_atual = cidade_mais_proxima

    custo_total += calcular_distancia(cidade_atual, cidades[0])
    return tour, custo_total

def custo_da_rota(tour, cidades_mapa):
    """Calcula o custo total de uma rota específica."""
    custo = 0
    for i in range(len(tour)):
        c1 = cidades_mapa[tour[i]]
        c2 = cidades_mapa[tour[(i + 1) % len(tour)]]
        custo += calcular_distancia(c1, c2)
    return custo

def otimizacao_2opt(tour_inicial, cidades):
    """Busca local para remover cruzamentos."""
    melhor_tour = tour_inicial[:]
    cidades_mapa = {c[0]: c for c in cidades}
    melhor_custo = custo_da_rota(melhor_tour, cidades_mapa)
    
    melhoria = True
    while melhoria:
        melhoria = False
        for i in range(1, len(melhor_tour) - 2):
            for j in range(i + 1, len(melhor_tour)):
                if j - i == 1: continue 
                
                novo_tour = melhor_tour[:]
                novo_tour[i:j] = melhor_tour[j-1:i-1:-1]
                
                novo_custo = custo_da_rota(novo_tour, cidades_mapa)
                
                if novo_custo < melhor_custo:
                    melhor_custo = novo_custo
                    melhor_tour = novo_tour
                    melhoria = True
                    break 
            if melhoria:
                break
                
    return melhor_tour, melhor_custo

def imprimir_saida(nome_instancia, custo, tour):
    """Imprime o resultado no formato exigido pela TSPLIB."""
    print(f"NAME: {nome_instancia}")
    # Atualizado com o trio completo do relatório
    print("COMMENT: Francisco Romário, Rodolfo Rodrigues e Hércules Bruno - Vizinho Mais Proximo + 2-Opt")
    print("TYPE: TOUR")
    print(f"DIMENSION: {len(tour)}")
    print(f"TOTAL WEIGHT: {custo}")
    print("TOUR_SECTION")
    for cidade_id in tour:
        print(cidade_id)
    print("EOF")

if __name__ == "__main__":
    nome_instancia = "desconhecido"
    cidades = []
    lendo_coordenadas = False
    
    # Leitura estrita via stdin
    for linha in sys.stdin:
        linha = linha.strip()
        if not linha or linha == "EOF":
            break
            
        if linha.startswith("NAME:"):
            nome_instancia = linha.split(":")[1].strip()
            
        if linha == "NODE_COORD_SECTION":
            lendo_coordenadas = True
            continue
            
        if lendo_coordenadas:
            partes = linha.split()
            if len(partes) >= 3:
                cidades.append((int(partes[0]), float(partes[1]), float(partes[2])))
    
    if cidades:
        num_cidades = len(cidades)
        cidades_mapa = {c[0]: c for c in cidades}
        
        # DEFINIÇÃO DE ESTRATÉGIA POR ESCALA (Ajuste Agressivo de Tempo para proteger o R_i)
        if num_cidades <= 76:
            passos_busca = num_cidades
        elif num_cidades <= 150:
            passos_busca = 10
        elif num_cidades <= 200:
            passos_busca = 2  # Protege o tempo na kroA200
        else:
            passos_busca = 1  # Instâncias gigantes (gil266) rodam apenas 1 vez!
            
        melhor_tour_global = []
        melhor_custo_global = float('inf')
        
        # Roda o algoritmo testando diferentes pontos de partida
        for i in range(passos_busca):
            # Rotaciona a lista para simular começar de uma cidade diferente
            cidades_rotacionadas = cidades[i:] + cidades[:i]
            
            tour_inicial, _ = vizinho_mais_proximo(cidades_rotacionadas)
            tour_otimizado, custo_otimizado = otimizacao_2opt(tour_inicial, cidades)
            
            if custo_otimizado < melhor_custo_global:
                melhor_custo_global = custo_otimizado
                melhor_tour_global = tour_otimizado
                
        # 3. Saída formatada imutável exigida pelo professor
        imprimir_saida(nome_instancia, melhor_custo_global, melhor_tour_global)