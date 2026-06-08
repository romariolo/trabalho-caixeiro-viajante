import os
import sys
import time
import subprocess

def medir_experimentos():
    print("=" * 65)
    print(" INICIANDO AVALIAÇÃO EXPERIMENTAL DOS ALGORITMOS (TSP)")
    print("=" * 65)
    print(f"{'Instância':<15} | {'Status':<10} | {'Tempo (s)':<15}")
    print("-" * 65)
    
    arquivos = [f for f in os.listdir('.') if f.endswith('.tsp')]
    
    if not arquivos:
        print("[AVISO] Nenhum arquivo .tsp encontrado na pasta.")
        return

    # Ordena os arquivos pelo tamanho real em bytes (garante que os menores rodem primeiro)
    arquivos.sort(key=lambda x: os.path.getsize(x))

    for arquivo_tsp in arquivos:
        arquivo_tour = arquivo_tsp + ".tour"
        
        print(f"Processando: {arquivo_tsp:<15} ", end="", flush=True)
        
        try:
            # 1. Lê o conteúdo do arquivo para a memória primeiro (evita travamento do Windows)
            with open(arquivo_tsp, 'r', encoding='utf-8', errors='ignore') as f:
                conteudo = f.read()
                
            tempo_inicio = time.perf_counter()
            
            # 2. Executa o subprocesso usando o executável exato do Python e injeta o texto
            resultado = subprocess.run(
                [sys.executable, 'tsp_solver.py'],
                input=conteudo,
                text=True,
                capture_output=True,
                check=True,
                timeout=120 # Se passar de 2 minutos, ele avisa em vez de travar
            )
            
            tempo_fim = time.perf_counter()
            tempo_total = tempo_fim - tempo_inicio
            
            # 3. Salva a resposta gerada no arquivo .tour
            with open(arquivo_tour, 'w', encoding='utf-8') as f:
                f.write(resultado.stdout)
                
            # Limpa a linha de 'Processando' e mostra o resultado
            print(f"\r{arquivo_tsp:<15} | {'Sucesso':<10} | {tempo_total:.6f} s")
            
        except subprocess.TimeoutExpired:
            print(f"\r{arquivo_tsp:<15} | {'Erro':<10} | Estourou o tempo limite de 2 min")
        except subprocess.CalledProcessError as e:
            print(f"\r{arquivo_tsp:<15} | {'Erro':<10} | Código de erro: {e.returncode}")
        except Exception as e:
            print(f"\r{arquivo_tsp:<15} | {'Erro':<10} | Falha: {str(e)[:30]}")

if __name__ == "__main__":
    medir_experimentos()