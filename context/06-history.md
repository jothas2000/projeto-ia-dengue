# Histórico

Registro cronológico dos checkpoints do projeto. O mais recente fica no topo.

---

## Checkpoint 1 — Implementação base completa
**25/09/2026**

Estado do projeto ao fim do checkpoint: **implementação básica completa e funcional**. Faltam as
execuções manuais, os gráficos e o relatório.

### O que foi feito

**Repositório**
- Criado `jothas2000/projeto-ia-dengue` no GitHub, público.
- `.gitignore` para Python, `README.md` com documentação completa, `requirements.txt`.
- Enunciado em PDF versionado na raiz para referência.

**Modelagem**
- `src/grid.py` — matriz com 4 tipos de célula, custos (livre 1, grama 2, difícil 4, obstáculo
  intransponível), função sucessora gerando vizinhos sob demanda (grafo implícito).
- `src/node.py` — nó da árvore de busca com ponteiro para o pai, e a estrutura `ResultadoBusca`
  que padroniza as métricas dos quatro algoritmos.

**Algoritmos** — todos autorais, em `src/search/`
- BFS (fila FIFO), DFS (pilha LIFO), Busca Gulosa (`f = h`), A* (`f = g + h`).
- Heurística: Manhattan × custo mínimo, admissível e consistente.

**Cenários** — `src/scenarios.py`
- Três níveis: 8×10 simples, 12×15 intermediário, 16×20 complexo.
- O cenário 3 foi desenhado para demonstrar menos passos ≠ menor custo, e cumpre o objetivo.

**Interface** — `src/ui.py`, `main.py`
- Menu de seleção, execução simultânea usuário/agente, painel de métricas ao vivo, visualização
  dos estados explorados, tela de resultados com comparação e mensagem educativa.

**Conteúdo educacional** — `src/educational.py`
- Dez tipos de foco com orientação de prevenção.

**Experimentos** — `experiments.py`, `src/metrics.py`
- As 12 execuções algorítmicas rodadas e exportadas para
  `results/execucoes_algoritmos.csv`.

### Verificações realizadas
- Os 4 algoritmos resolvem todos os focos dos 3 cenários.
- A* devolve o menor custo em todos os casos; BFS, o menor número de passos.
- As 12 combinações cenário × algoritmo renderizam sem erro na interface.
- Movimentos inválidos bloqueados; gravação do CSV do usuário funcionando.

### Resultado que sustenta o projeto
Cenário 3: BFS encontra 17 passos com custo 68; A* encontra 23 passos com custo 38. A exigência
central do enunciado está demonstrada com números próprios.

### Ajuste feito durante o checkpoint
Primeira versão da interface usava azul tanto para o rastro do usuário quanto para os estados
explorados, e os dois se confundiam na tela. Estados explorados passaram para lilás e o rastro
do usuário ficou maior.

### Entregáveis do checkpoint
- Código no GitHub: https://github.com/jothas2000/projeto-ia-dengue
- Guia de estudo: https://claude.ai/code/artifact/e077850e-6f61-4233-bf35-dcca5a01b8b7
- Esta pasta `context/`.

### Próximo passo
Jogar as 3 missões manuais (`python main.py`, um cenário por vez, sem repetir) para completar as
15 execuções exigidas. Detalhes em `02-next-steps.md`.

---

## Checkpoint 0 — Análise do enunciado
**25/09/2026**

Leitura das 16 páginas do enunciado e levantamento dos requisitos. Definição da abordagem:
Python + Pygame, algoritmos autorais, três cenários com o terceiro desenhado para demonstrar a
divergência entre passos e custo. Repositório criado no GitHub para acesso da equipe.
