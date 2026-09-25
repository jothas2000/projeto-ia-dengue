# Decisões técnicas e por quê

Este arquivo existe para a **defesa oral**. Cada integrante precisa conseguir explicar qualquer
decisão abaixo. Não é "o que o código faz" — é *por que foi feito assim*.

---

## Por que Python + Pygame

O enunciado não fixa linguagem. Python foi escolhido porque as estruturas de dados necessárias
(`deque` para fila, `list` para pilha, `heapq` para fila de prioridade) estão na biblioteca
padrão, e Pygame dá controle direto sobre desenho e teclado sem arrastar um framework pesado.

**Cuidado na defesa:** o enunciado proíbe "bibliotecas prontas para os algoritmos de busca".
`heapq` **não** viola isso — ele é uma fila de prioridade genérica, uma estrutura de dados. Os
algoritmos (a lógica de expansão, o controle de visitados, a função de avaliação, a reconstrução
do caminho) são todos autorais. Seria violação usar, por exemplo, `networkx.astar_path`.

---

## Por que o grafo é implícito

O enunciado é explícito: "não é necessário construir previamente um grafo explícito com todos os
nós e arestas". Construir o grafo inteiro para um mapa 16×20 significaria criar 320 nós e suas
arestas antes de saber se serão usados.

`Grid.sucessores(posicao)` gera os vizinhos sob demanda. A Busca Gulosa no cenário 3 expande
apenas 18 estados — dos 320 possíveis. Materializar o grafo teria sido desperdício de 94% do
trabalho.

---

## Por que o custo é cobrado ao entrar na célula

Duas convenções eram possíveis: cobrar ao sair ou cobrar ao entrar. Escolhemos **ao entrar**,
porque é a que torna o custo uma propriedade do terreno pisado, e não da origem do movimento.

Consequência: a posição inicial nunca entra na soma, já que nunca se "entra" nela.
Ver `Grid.custo_do_caminho()` — soma a partir de `caminho[1:]`.

---

## Por que a ordem de ações é fixa (cima, baixo, esquerda, direita)

Empates são frequentes num grid. Se a ordem de geração dos sucessores variasse entre execuções,
dois experimentos idênticos poderiam devolver caminhos diferentes — e a análise comparativa do
relatório perderia o chão.

A ordem está fixa na constante `ACOES` em `src/grid.py`. Na DFS a lista é percorrida invertida
(`reversed`) antes de empilhar, para que a pilha desempilhe na mesma ordem em que a BFS enfileira.
Sem isso, os dois algoritmos explorariam o mapa em ordens espelhadas, dificultando a comparação.

---

## Por que existe um contador de desempate na fila de prioridade

`heapq` compara tuplas elemento a elemento. Com `(f, no)`, dois nós de mesmo `f` fariam o Python
tentar comparar dois objetos `No` — que não definem `<` — levantando `TypeError`.

A solução é inserir `(f, contador, no)`, com o contador incrementando a cada inserção. Ele
nunca empata, então a comparação nunca chega ao terceiro elemento. Como o contador cresce
monotonicamente, o desempate é **FIFO**: entre nós de mesmo `f`, vence o que entrou primeiro.
Comportamento determinístico e reproduzível.

---

## Por que a heurística multiplica pelo custo mínimo

`h(n) = manhattan(n, objetivo) × custo_mínimo`, com `custo_mínimo = 1`.

**Admissibilidade:** a Distância Manhattan é o número mínimo de movimentos até o objetivo — com
apenas movimentos ortogonais, nenhum caminho legal usa menos. Cada movimento custa no mínimo 1.
Logo o produto é um piso do custo real: `h(n) ≤ h*(n)`.

**Consistência:** um movimento altera a Manhattan em exatamente 1, então
`h(n) − h(n') ≤ 1 ≤ custo(n, n')`. Consistência implica admissibilidade, e garante que ao
expandir um nó o A* já encontrou o melhor caminho até ele.

**O erro que evitamos:** multiplicar pelo custo médio (2) ou máximo (4) faria a heurística
superestimar em qualquer trecho de terreno barato — e o A* deixaria de garantir o caminho ótimo.

---

## Por que o cenário 3 foi desenhado assim

O enunciado exige que o terceiro cenário "permita observar situações em que o caminho com menor
quantidade de passos não corresponda necessariamente ao caminho de menor custo". Isso não
acontece por acaso — precisou ser construído.

A construção: uma faixa horizontal de terreno difícil (custo 4) atravessando o mapa inteiro,
com **partida e foco dentro dela**, em lados opostos. A linha reta entre os dois é curta em
passos e cara em custo; a calçada livre acima exige subir, atravessar e descer — mais passos,
custo muito menor.

Números: BFS faz 17 passos × 4 = 68. A* faz 3×4 (subindo) + 17×1 (calçada) + 3×4 (descendo) =
9 + 17 + 12 = 38, em 23 passos. Seis passos a mais, 44% menos custo.

---

## Por que a busca do agente roda instantaneamente e só depois anima

A seção 2.4.3 do enunciado determina: "o tempo de execução do algoritmo deverá ser medido
separadamente do tempo utilizado para a representação visual do deslocamento do agente".

Se a busca avançasse um nó por quadro de animação, o tempo medido seria o tempo do Pygame, não
o do algoritmo — e todos os quatro pareceriam igualmente lentos. `Jogo.iniciar_missao()` resolve
a busca inteira de uma vez, guarda `resultado.tempo` (medido com `time.perf_counter()` dentro do
próprio algoritmo), e a animação percorre o caminho já encontrado.

---

## Por que a missão só termina quando ambos chegam

Também vem do enunciado: "a missão deverá permanecer ativa até que usuário e agente tenham
alcançado o foco, mesmo que um deles chegue antes". Se encerrasse no primeiro a chegar, o agente
quase sempre venceria (ele anima em ~180 ms por passo, sem hesitar) e a métrica do usuário ficaria
incompleta.

---

## Por que os estados explorados aparecem progressivamente

Mostrar todos os estados explorados de uma vez, no instante inicial, entregaria a resposta ao
jogador antes de ele se mover. `indice_agente_explorado()` revela os estados proporcionalmente ao
avanço do agente no caminho, preservando a comparação — e tornando visível *quanto* cada
algoritmo explorou. O contraste entre a Gulosa (18 células) e a BFS (199) fica evidente na tela.

---

## Por que as cores são as que são

Terrenos usam cores naturalistas (grama verde, terreno difícil em tom de terra) para leitura
imediata. Usuário é azul, agente é vermelho, estados explorados são lilás — três matizes
distintos, escolhidos depois de uma primeira versão em que o rastro do usuário e os estados
explorados eram ambos azuis e se confundiam na tela.

Pensando no bônus (público com deficiência intelectual e crianças), a distinção por matiz
importa mais do que a estética.
