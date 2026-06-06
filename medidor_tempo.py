import os
import time
import subprocess

# ==========================================
# REGISTRO DE USO DE IA (Para o Relatório)
# Prompt utilizado: "Crie um script em Python auxiliar que liste arquivos .tsp em uma pasta, execute o script principal passando a entrada por stdin, meça o tempo exato de execução em segundos e exiba um resumo de benchmark para análise experimental."
# ==========================================

def medir_experimentos():
    print("=" * 60)
    print(" INICIANDO AVALIAÇÃO EXPERIMENTAL DOS ALGORITMOS (TSP)")
    print("=" * 60)
    print(f"{'Instância':<20} | {'Status':<10} | {'Tempo de Execução (s)':<22}")
    print("-" * 60)
    
    # Procura arquivos .tsp na pasta atual
    arquivos = [f for f in os.listdir('.') if f.endswith('.tsp')]
    
    if not arquivos:
        print("[AVISO] Nenhum arquivo .tsp encontrado na pasta para teste.")
        print("Coloque as instâncias (ex: tulio5.tsp) nesta mesma pasta.")
        return

    for arquivo_tsp in arquivos:
        arquivo_tour = arquivo_tsp + ".tour"
        
        # Registra o tempo de início de alta precisão
        tempo_inicio = time.perf_counter()
        
        try:
            # Executa o tsp_solver.py injetando o arquivo no stdin e salvando no stdout
            # Exatamente como a execução por linha de comando exigida
            with open(arquivo_tsp, 'r') as entrada:
                with open(arquivo_tour, 'w') as saida:
                    subprocess.run(
                        ['python', 'tsp_solver.py'],
                        stdin=entrada,
                        stdout=saida,
                        check=True
                    )
            
            tempo_fim = time.perf_counter()
            tempo_total = tempo_fim - tempo_inicio
            
            print(f"{arquivo_tsp:<20} | {'Sucesso':<10} | {tempo_total:.6f} segundos")
            
        except Exception as e:
            print(f"{arquivo_tsp:<20} | {'Erro':<10} | Falha na execução: {e}")

if __name__ == "__main__":
    medir_experimentos()