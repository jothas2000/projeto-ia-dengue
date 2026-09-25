# O que documentar

As 10 seções exigidas pelo Apêndice A do enunciado, com a pontuação de cada uma e o que já
temos pronto para preencher.

**Total: 1,0 ponto.** A avaliação considera presença **e** profundidade — seção rasa não
pontua integralmente.

---

## 1. Introdução — 0,05

**O que pedem:** apresentar o problema da dengue, o objetivo do projeto e os algoritmos
implementados. Abordar a importância da representação em espaços de estados, do uso de
algoritmos de busca e da comparação usuário × agente.

**Material disponível:** README + seção 01 do artifact de estudo.

---

## 2. Modelagem do Problema — 0,15

**O que pedem:** como o ambiente foi representado computacionalmente — matriz, dimensões, tipos
de células, posição inicial, focos, obstáculos, terrenos e custos. Explicar como a matriz
corresponde a um grafo implícito, indicando estados, ações, função sucessora, teste de objetivo
e custo do caminho.

**Material disponível:** tabela de formulação completa em `01-onde-estamos.md` e na seção 02 do
artifact. Código de referência: `src/grid.py`.

**Não esquecer:** justificar os valores de custo escolhidos (1, 2, 4). O enunciado permite
alterá-los "desde que positivos, coerentes com o problema e devidamente justificados".

---

## 3. Desenvolvimento e Funcionamento do Ambiente — 0,10

**O que pedem:** funcionamento geral da simulação, interação do usuário e atuação do agente.
Como são definidos cenários, posição inicial e foco. **Como garantimos que usuário e agente
resolvem a mesma instância.** Como ocorre a execução de ambos, como o usuário se move e como o
deslocamento do agente é apresentado visualmente.

**Material disponível:** seção "Interface gráfica" de `01-onde-estamos.md`.

**Ponto forte a destacar:** o tempo do algoritmo é medido separadamente do tempo de animação
(exigência da seção 2.4.3 do enunciado) — o agente resolve a busca inteira no instante em que a
missão começa, e só depois anima o caminho. Ver `Jogo.iniciar_missao` em `src/ui.py`.

---

## 4. Implementação dos Algoritmos — 0,15

**O que pedem:** descrição detalhada de BFS, DFS, Gulosa e A*. Para cada um: funcionamento,
estruturas de dados, tratamento dos estados visitados, geração dos sucessores e reconstrução do
caminho final. Para Gulosa e A*, apresentar as funções de avaliação.

**Material disponível:** os quatro cards da seção 03 do artifact e o pseudocódigo do esqueleto
comum. Código: `src/search/`.

**Não esquecer:**
- A reconstrução do caminho é feita por ponteiro para o pai (`No.caminho()` em `src/node.py`).
- BFS testa o objetivo **na geração** do sucessor, não na expansão — por isso não precisa
  expandir o nó objetivo.
- O contador de desempate na fila de prioridade, e por que ele é necessário.

---

## 5. Heurística Utilizada — 0,10

**O que pedem:** fórmula, como é calculada, por que é adequada, relação com os custos de
deslocamento, e discussão sobre **admissibilidade** e, quando pertinente, **consistência**.

**Material disponível:** seção 04 do artifact, com as duas demonstrações escritas.
Código: `src/search/heuristics.py`.

**Este é o item mais fácil de perder ponto por superficialidade.** Não basta dizer "usamos
Manhattan". Precisa demonstrar por que multiplicar pelo custo **mínimo** preserva a
admissibilidade, e o que aconteceria se usássemos o custo médio ou máximo.

---

## 6. Conteúdo Educacional — 0,05

**O que pedem:** os tipos de foco usados no ambiente e as informações educativas associadas a
cada um. Como essas informações são apresentadas ao usuário. **Citar as fontes confiáveis.**

**Material disponível:** `src/educational.py`, com 10 tipos de foco.

**Falta fazer:** levantar e citar as referências reais (Ministério da Saúde, Fiocruz), com URL e
data de acesso, em formato ABNT. As mensagens foram redigidas com base nessas orientações, mas
as referências precisam ser conferidas e formalizadas.

---

## 7. Experimentos Realizados — 0,15

**O que pedem:** descrição dos cenários (características, complexidade, posição inicial, foco,
obstáculos, custos). As execuções do usuário e dos quatro algoritmos, organizadas em tabelas e,
quando pertinente, gráficos.

**Material disponível:** `results/execucoes_algoritmos.csv` e a tabela em `01-onde-estamos.md`.

**Falta:** as 3 execuções manuais e os gráficos (ver `02-para-onde-vamos.md`, itens 1 e 2).

**Formato de tabela sugerido pelo enunciado:**
`Cenário | Método | Passos | Custo | Tempo | Estados Expandidos | Estados Gerados | Etc`
Nas linhas do usuário, as colunas de expandidos/gerados/fronteira ficam com `—`.

---

## 8. Análise dos Resultados — 0,15

**O que pedem:** interpretar e comparar, **sem se limitar a apresentar valores numéricos**. O
enunciado lista 11 questões no Apêndice A e 15 na seção 2.9 — e diz explicitamente que a
análise não deve se limitar a elas.

**Material disponível:** as 15 questões já respondidas com os nossos números, na seção 07 do
artifact de estudo.

**Atenção:** as questões 11 a 14 dependem das execuções manuais e ainda não têm resposta
definitiva. As respostas no artifact são hipóteses a confirmar depois de jogar.

---

## 9. Conclusão — 0,05

**O que pedem:** principais resultados e aprendizados, destacando a comparação entre estratégias
de busca e entre solução humana e algorítmica. Discutir **limitações da implementação,
dificuldades encontradas e possíveis melhorias ou extensões**.

**Limitações honestas que podemos citar:**
- Movimentação restrita a 4 direções, sem diagonais.
- Ambiente estático: os focos não se multiplicam nem mudam ao longo do tempo.
- Um único objetivo por missão — não há problema de múltiplos focos em sequência
  (que seria um problema de roteamento, não de busca simples).
- A comparação com o usuário depende de uma amostra de uma única pessoa por cenário.

---

## 10. Referências / Organização textual — 0,05

**O que pedem:** referências adequadas em ABNT, clareza, organização e qualidade geral da
escrita.

**Referências que certamente vão entrar:**
- Livro-texto de IA da disciplina (Russell & Norvig, provavelmente) — para os algoritmos de
  busca, admissibilidade e consistência.
- Ministério da Saúde — orientações de prevenção da dengue.
- Fundação Oswaldo Cruz (Fiocruz) — idem.
- Documentação do Pygame, se citarmos a biblioteca.

---

## Lembrete sobre formatação

Usar o modelo oficial da UTFPR para trabalhos acadêmicos regulares **sem licença Creative
Commons**, disponível em:
https://www.utfpr.edu.br/bibliotecas/trabalhos-academicos/orientacoes-para-entrega
