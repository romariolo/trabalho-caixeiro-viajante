# 🗺️ Solver: Problema do Caixeiro Viajante (TSP)

Este repositório contém a implementação de um solver heurístico para o clássico Problema do Caixeiro Viajante (TSP), focado em instâncias simétricas bidimensionais (EUC_2D) no formato padrão da TSPLIB.

Desenvolvido como trabalho prático acadêmico, o algoritmo busca um equilíbrio ótimo entre Qualidade da Solução ($Q_i$) e Tempo de Execução ($R_i$).

## 🚀 Tecnologias e Algoritmos
- **Linguagem:** Python 3.x
- **Heurística Construtiva:** Vizinho Mais Próximo (*Nearest Neighbor*)
- **Busca Local (Refinamento):** 2-Opt
- **Estratégia de Competição:** Multi-start Dinâmico (rotaciona o vértice de partida com base na escala da instância para evitar mínimos locais e proteger o tempo de processamento).

## 📁 Estrutura do Repositório

- `tsp_solver.py`: O núcleo do projeto. Lê os arquivos `.tsp` via `stdin`, processa a rota e imprime o resultado formatado no `stdout`.
- `medidor_tempo.py`: Script de automação para análise experimental. Roda o solver em todas as instâncias da pasta e gera um log de tempo de execução.
- `plotador_tsp.py`: Utilitário visual que utiliza a biblioteca `matplotlib` para gerar gráficos (.png) das rotas encontradas.
- `documentacao_tsp.html`: Documentação interativa da arquitetura do projeto.

## ⚙️ Como Executar

O projeto foi construído para rodar nativamente via terminal, sem necessidade de dependências externas para o motor principal.

**1. Executar o Solver Principal:**
Para rodar uma instância específica (ex: `tulio5.tsp`) e gerar o arquivo da rota (`.tour`):

No Prompt de Comando (CMD) ou Linux/bash:
```bash
python tsp_solver.py < tulio5.tsp > tulio5.tsp.tour