# Projeto 1 — Agente de Combate à Dengue

Disciplina: **Inteligência Artificial** — Bacharelado em Ciência da Computação (BCC)
Universidade Tecnológica Federal do Paraná (UTFPR) — Campus Ponta Grossa

Resolução de problema por meio de algoritmos de busca: um **usuário** (controle manual) e um
**agente inteligente** (algoritmo de busca) resolvem a mesma instância do problema — mesmo
cenário, mesma posição inicial e mesmo foco de dengue como objetivo — permitindo comparar a
decisão humana com a decisão algorítmica.

> **Acompanhando o projeto?** A pasta [`contexto/`](contexto/) é o diário de bordo: em que passo
> estamos, para onde vamos, o que falta testar e documentar. Comece por
> [`contexto/00-LEIA-PRIMEIRO.md`](contexto/00-LEIA-PRIMEIRO.md).

## Requisitos

- Python 3.10 ou superior
- Pygame

```bash
pip install -r requirements.txt
```

## Como executar

**Ambiente de simulação (jogo):**

```bash
python main.py
```

**Experimentos automáticos (12 execuções algorítmicas, sem interface):**

```bash
python experiments.py
```

Os resultados são salvos em `results/execucoes_algoritmos.csv`. As execuções manuais feitas no
jogo são registradas automaticamente em `results/execucoes_usuario.csv`.

## Controles

| Tela | Tecla | Ação |
|---|---|---|
| Menu | ↑ / ↓ | Escolher a opção (cenário, foco, algoritmo) |
| Menu | ← / → | Alterar o valor da opção |
| Menu | ENTER | Iniciar a missão |
| Jogo | Setas / WASD | Mover o usuário |
| Jogo | E | Mostrar ou ocultar os estados explorados pelo algoritmo |
| Jogo | R | Reiniciar a missão |
| Jogo | ESC | Voltar ao menu |

A missão só termina quando **ambos** — usuário e agente — alcançam o foco, mesmo que um chegue
antes do outro.

## Modelagem do problema

O ambiente é uma matriz bidimensional tratada como **grafo implícito**: os sucessores são
gerados dinamicamente pela função `Grid.sucessores`, sem construção prévia de nós e arestas.

| Elemento | Definição |
|---|---|
| **Estado inicial** | Posição de origem da missão, idêntica para usuário e agente |
| **Estado objetivo** | Posição do foco de dengue selecionado |
| **Estados** | Todas as posições válidas (dentro da matriz e não obstáculo) |
| **Ações** | Mover para cima, baixo, esquerda e direita |
| **Função sucessora** | Posições adjacentes válidas a partir da posição atual |
| **Teste de objetivo** | Posição atual igual à posição do foco |
| **Custo do caminho** | Soma dos custos das células percorridas (exceto a inicial) |

### Custos de deslocamento

| Tipo de célula | Símbolo no mapa | Custo |
|---|---|---|
| Caminho livre / calçada | `.` | 1 |
| Grama | `g` | 2 |
| Terreno de difícil acesso | `d` | 4 |
| Obstáculo | `#` | não permitido |

## Algoritmos implementados

Todos implementados do zero, sem uso de bibliotecas prontas de busca.

| Algoritmo | Estratégia | Arquivo |
|---|---|---|
| **BFS** | Fila FIFO, explora por níveis | `src/search/bfs.py` |
| **DFS** | Pilha LIFO, aprofunda um ramo antes de alternativas | `src/search/dfs.py` |
| **Busca Gulosa** | Fila de prioridade por `f(n) = h(n)` | `src/search/greedy.py` |
| **A\*** | Fila de prioridade por `f(n) = g(n) + h(n)` | `src/search/astar.py` |

### Heurística

`h(n) = distância_manhattan(n, objetivo) × custo_mínimo_de_movimento`

A Distância Manhattan corresponde ao número mínimo de movimentos até o objetivo. Como todo
movimento custa no mínimo `custo_mínimo` (1, no caminho livre), multiplicar a distância por esse
valor garante que `h(n)` **nunca superestime** o custo real restante — mantendo a heurística
**admissível** e **consistente** mesmo com terrenos de custos diferentes. É por isso que o A\*
encontra o caminho de menor custo em todos os cenários.

## Cenários

| Cenário | Dimensões | Característica |
|---|---|---|
| 1 — Simples | 8×10 | Poucos obstáculos, custos predominantemente uniformes |
| 2 — Intermediário | 12×15 | Mais obstáculos, múltiplas possibilidades de caminho |
| 3 — Complexo | 16×20 | Faixa central de terreno difícil; menos passos ≠ menor custo |

## Resultados obtidos

Execuções algorítmicas sobre o foco padrão de cada cenário:

| Cenário | Método | Passos | Custo | Expandidos | Gerados | Fronteira |
|---|---|---|---|---|---|---|
| 1 — Simples | BFS | 16 | 16 | 70 | 72 | 8 |
| 1 — Simples | DFS | 62 | 66 | 72 | 119 | 48 |
| 1 — Simples | Gulosa | 16 | 16 | 17 | 32 | 16 |
| 1 — Simples | A\* | 16 | 16 | 64 | 71 | 11 |
| 2 — Intermediário | BFS | 12 | 12 | 50 | 58 | 8 |
| 2 — Intermediário | DFS | 76 | 84 | 101 | 149 | 45 |
| 2 — Intermediário | Gulosa | 16 | 16 | 21 | 34 | 12 |
| 2 — Intermediário | A\* | 12 | 12 | 26 | 36 | 11 |
| 3 — Complexo | BFS | 17 | **68** | 199 | 212 | 17 |
| 3 — Complexo | DFS | 207 | 389 | 259 | 464 | 194 |
| 3 — Complexo | Gulosa | 17 | **68** | 18 | 41 | 24 |
| 3 — Complexo | A\* | **23** | **38** | 256 | 289 | 80 |

Observações principais para a análise do relatório:

- **Cenário 3** evidencia que o caminho com menos passos não é o de menor custo: BFS e Gulosa
  atravessam a faixa de terreno difícil em 17 passos, mas pagam custo 68; o A\* contorna por
  cima usando 23 passos e custo 38.
- **A Busca Gulosa é a mais econômica em exploração** (18 estados expandidos no cenário 3), mas
  não garante solução ótima — no cenário 2 encontra 16 passos onde o ótimo são 12.
- **DFS apresenta o pior comportamento** em todos os cenários, tanto em custo quanto em
  quantidade de passos, por aprofundar ramos sem qualquer critério de qualidade.
- **A\* é o único que encontra o caminho de menor custo em todos os cenários**, ao preço de
  expandir mais estados que a Gulosa.

## Estrutura do repositório

```
Projeto1/
├── main.py                    # ponto de entrada do jogo
├── experiments.py             # executa as 12 execuções algorítmicas e exporta CSV
├── requirements.txt
├── src/
│   ├── grid.py                # ambiente, tipos de célula, custos, função sucessora
│   ├── node.py                # nó da árvore de busca e estrutura de resultado
│   ├── scenarios.py           # os três cenários
│   ├── educational.py         # mensagens de prevenção por tipo de foco
│   ├── metrics.py             # registro e exportação de métricas
│   ├── ui.py                  # interface gráfica (Pygame)
│   └── search/
│       ├── heuristics.py
│       ├── bfs.py
│       ├── dfs.py
│       ├── greedy.py
│       └── astar.py
├── results/                   # CSVs gerados pelas execuções
└── Projeto nº 1 - Agente de Combate a Dengue [04-09-26].pdf
```

## Conteúdo educacional

Ao alcançar um foco, o sistema apresenta uma orientação de prevenção específica para aquele tipo
de criadouro (pneu, prato de vaso, garrafa, caixa-d'água, calha, piscina, entre outros). As
mensagens estão em `src/educational.py` e são baseadas nas orientações do Ministério da Saúde e
da Fundação Oswaldo Cruz (Fiocruz).

## Equipe

- Thales Prado ([@jothas2000](https://github.com/jothas2000))
- _adicionar demais integrantes_

## Cronograma

- Entrega no Moodle: **02/10/2026**
- Apresentação presencial: a partir de **05/10/2026**
