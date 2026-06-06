import matplotlib.pyplot as plt
import sys
import os

def ler_coordenadas(caminho_tsp):
    cidades = {}
    lendo = False
    with open(caminho_tsp, 'r') as f:
        for linha in f:
            linha = linha.strip()
            if linha == "NODE_COORD_SECTION":
                lendo = True
                continue
            if linha == "EOF":
                break
            if lendo:
                partes = linha.split()
                if len(partes) >= 3:
                    cidades[int(partes[0])] = (float(partes[1]), float(partes[2]))
    return cidades

def ler_tour(caminho_tour):
    tour = []
    lendo = False
    with open(caminho_tour, 'r') as f:
        for linha in f:
            linha = linha.strip()
            if linha == "TOUR_SECTION":
                lendo = True
                continue
            if linha == "-1" or linha == "EOF":
                break
            if lendo:
                try:
                    tour.append(int(linha))
                except ValueError:
                    pass
    return tour

def plotar_grafo(arquivo_tsp, arquivo_tour=None):
    if not os.path.exists(arquivo_tsp):
        print(f"Arquivo não encontrado: {arquivo_tsp}")
        return

    cidades = ler_coordenadas(arquivo_tsp)
    x = [cidades[i][0] for i in cidades]
    y = [cidades[i][1] for i in cidades]

    plt.figure(figsize=(10, 8))
    
    # Plota os pontos (Cidades)
    plt.scatter(x, y, c='red', s=30, zorder=5, label='Cidades')

    # Plota a rota se o arquivo .tour existir
    if arquivo_tour and os.path.exists(arquivo_tour):
        tour = ler_tour(arquivo_tour)
        if tour:
            # Garante que o caminho fecha o ciclo ligando o último ao primeiro
            tour_fechado = tour + [tour[0]]
            x_tour = [cidades[i][0] for i in tour_fechado]
            y_tour = [cidades[i][1] for i in tour_fechado]
            
            plt.plot(x_tour, y_tour, c='blue', linewidth=1.5, zorder=1, label='Rota Otimizada')
            plt.title(f"Solução TSP: {os.path.basename(arquivo_tsp)}\nCusto Total (Aprox): Avalie no Tour")
    else:
        plt.title(f"Instância TSP: {os.path.basename(arquivo_tsp)} (Sem Rota)")

    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    nome_saida = arquivo_tsp + "_plot.png"
    plt.savefig(nome_saida, dpi=300)
    print(f"Gráfico salvo com sucesso: {nome_saida}")
    
    # Descomente a linha abaixo se quiser que a janela abra na tela além de salvar o arquivo
    # plt.show()

if __name__ == "__main__":
    print("Gerador de Gráficos TSP")
    # Tenta encontrar o tulio5.tsp como exemplo padrão
    tsp_file = "tulio5.tsp"
    tour_file = "tulio5.tsp.tour"
    
    plotar_grafo(tsp_file, tour_file)