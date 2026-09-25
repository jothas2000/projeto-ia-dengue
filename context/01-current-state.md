# Onde estamos

**Checkpoint 1 — Implementação base completa e funcional**
Data: 25/09/2026

## Resumo em uma frase

O ambiente de simulação está inteiro: os quatro algoritmos funcionam, os três cenários existem,
a interface gráfica roda, e as 12 execuções algorítmicas já foram geradas. Falta a parte humana
(3 execuções manuais), os gráficos e o relatório.

## O que está pronto e verificado

### Modelagem do ambiente — `src/grid.py`, `src/node.py`
- Matriz bidimensional com 4 tipos de célula: livre (custo 1), grama (2), difícil (4), obstáculo.
- Tratada como **grafo implícito**: `Grid.sucessores()` gera os vizinhos sob demanda, sem
  construir lista de adjacência.
- Movimentos restritos a cima, baixo, esquerda e direita, em ordem fixa — resultados reproduzíveis.
- Custo cobrado ao *entrar* numa célula; a posição inicial não entra na soma.

### Os quatro algoritmos — `src/search/`
Todos implementados do zero, sem biblioteca de busca. Todos coletam: caminho, passos, custo,
estados expandidos, estados gerados, fronteira máxima, tempo e ordem de exploração.

| Arquivo | Algoritmo | Estrutura da fronteira |
|---|---|---|
| `bfs.py` | Busca em Largura | `collections.deque` (FIFO) |
| `dfs.py` | Busca em Profundidade | `list` como pilha (LIFO) |
| `greedy.py` | Busca Gulosa | `heapq` ordenado por `h(n)` |
| `astar.py` | A* | `heapq` ordenado por `g(n) + h(n)` |

### Heurística — `src/search/heuristics.py`
`h(n) = distância_manhattan(n, objetivo) × custo_mínimo`, com `custo_mínimo = 1`.
Admissível e consistente — justificativa completa em `05-technical-decisions.md`.

### Cenários — `src/scenarios.py`
| Cenário | Dimensões | Focos | Característica |
|---|---|---|---|
| 1 — Simples | 8×10 | 2 | Poucos obstáculos, custos quase uniformes |
| 2 — Intermediário | 12×15 | 3 | Labirinto de obstáculos, pátio interno |
| 3 — Complexo | 16×20 | 3 | Faixa central de terreno difícil |

O cenário 3 foi **desenhado deliberadamente** para cumprir a exigência do enunciado de que
menos passos ≠ menor custo. Confirmado nos dados: BFS faz 17 passos por custo 68; A* faz 23
passos por custo 38.

### Interface gráfica — `src/ui.py`, `main.py`
- Menu de seleção: cenário, foco e algoritmo do agente.
- Usuário move com setas/WASD; movimentos inválidos e obstáculos são bloqueados.
- Agente anima o caminho encontrado; estados explorados visíveis (alterna com `E`).
- Painel lateral com métricas ao vivo de ambos os participantes.
- A missão só encerra quando **ambos** alcançam o foco, conforme seção 2.4.3 do enunciado.
- Tela de resultados com comparação usuário × agente e a mensagem educativa do foco.
- Execuções manuais gravadas automaticamente em `results/execucoes_usuario.csv`.

### Conteúdo educacional — `src/educational.py`
Dez tipos de foco com orientação de prevenção: pneu, prato de vaso, garrafa, balde,
caixa-d'água, calha, ralo, lixo, piscina e bebedouro de animais.

### Experimentos — `experiments.py`
Roda as 12 execuções algorítmicas sem interface gráfica e exporta
`results/execucoes_algoritmos.csv`. Usa mediana de N repetições para estabilizar a medição
de tempo.

## Resultados já obtidos

| Cenário | Método | Passos | Custo | Expandidos | Gerados | Fronteira |
|---|---|---|---|---|---|---|
| 1 — Simples | BFS | 16 | 16 | 70 | 72 | 8 |
| 1 — Simples | DFS | 62 | 66 | 72 | 119 | 48 |
| 1 — Simples | Gulosa | 16 | 16 | 17 | 32 | 16 |
| 1 — Simples | A* | 16 | 16 | 64 | 71 | 11 |
| 2 — Intermediário | BFS | 12 | 12 | 50 | 58 | 8 |
| 2 — Intermediário | DFS | 76 | 84 | 101 | 149 | 45 |
| 2 — Intermediário | Gulosa | 16 | 16 | 21 | 34 | 12 |
| 2 — Intermediário | A* | 12 | 12 | 26 | 36 | 11 |
| 3 — Complexo | BFS | 17 | **68** | 199 | 212 | 17 |
| 3 — Complexo | DFS | 207 | 389 | 259 | 464 | 194 |
| 3 — Complexo | Gulosa | 17 | **68** | 18 | 41 | 24 |
| 3 — Complexo | A* | **23** | **38** | 256 | 289 | 80 |

## O que NÃO está pronto

- As **3 execuções manuais** do usuário (uma por cenário).
- Os **gráficos** comparativos para o relatório.
- O **relatório técnico** (10 seções do Apêndice A).
- O **bônus** de jogo educacional (opcional, até +1,5 ponto).
- Os **nomes dos demais integrantes** no README (só consta Thales Prado).

## Como rodar

```bash
pip install -r requirements.txt
python main.py           # o jogo
python experiments.py    # as 12 execuções algorítmicas
```
