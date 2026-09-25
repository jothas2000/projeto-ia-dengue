# Para onde vamos

Ordem de prioridade. Os itens 1 a 4 são **obrigatórios** para a nota de 3,5 pontos. O item 5 é
bônus e só deve ser encostado depois que 1 a 4 estiverem fechados.

---

## 1. Executar as 3 missões manuais — *falta fazer*

**Por quê:** o enunciado exige 3 execuções humanas + 12 algorítmicas = 15 execuções. Sem as
manuais não existe a comparação usuário × agente, que é metade da análise.

**Como:**
```bash
python main.py
```
Jogar **uma única vez cada cenário**, usando o foco padrão (o primeiro da lista, que já vem
selecionado). O jogo grava sozinho em `results/execucoes_usuario.csv`.

**Regra importante do enunciado (seção 2.4.3):** uma execução manual por cenário, só. Repetir o
mesmo cenário contamina o resultado, porque o jogador aprende o mapa e deixa de representar uma
decisão humana genuína.

**Quem faz:** idealmente o mesmo integrante nos três cenários, para manter a comparação coerente.
Anotar no relatório quem jogou.

---

## 2. Gerar os gráficos comparativos — *falta fazer*

**Por quê:** o Apêndice A, seção 7, pede os resultados "em tabelas e, quando pertinente,
gráficos". Tabela já temos; gráfico ainda não.

**O que plotar** (sugestão — 3 gráficos bastam):
- Custo final por algoritmo, agrupado por cenário (barras). Mostra o A* ganhando.
- Estados expandidos por algoritmo, agrupado por cenário (barras, escala log se precisar).
  Mostra a Gulosa explorando quase nada.
- Passos × custo no cenário 3 (barras lado a lado). É o gráfico que prova a tese do projeto.

**Como:** criar `graficos.py` lendo `results/execucoes_algoritmos.csv` com `pandas` +
`matplotlib`, salvando PNGs em `results/`. Adicionar `pandas` e `matplotlib` ao
`requirements.txt`.

---

## 3. Escrever o relatório técnico — *falta fazer*

**Por quê:** vale 1,0 ponto e é condicionado à implementação estar completa (já está).

Ver `04-report-requirements.md` para o detalhamento das 10 seções. Usar o modelo de trabalhos
acadêmicos da UTFPR (link no enunciado, seção 1.2.2), formatação ABNT.

**Atenção:** a avaliação considera "tanto a presença das seções solicitadas quanto a qualidade,
correção e profundidade". Seção presente mas rasa não pontua integralmente.

---

## 4. Preparar a defesa — *falta fazer*

**Por quê:** 0,5 ponto, presencial e obrigatória, com **pergunta individual para cada
integrante**. Ausência conta falta como prova escrita.

**Como:** todos os integrantes precisam saber explicar qualquer parte do código. O artifact de
estudo (link em `00-README-FIRST.md`) traz as 15 questões da análise comparativa já respondidas
com os nossos números — usar como roteiro de estudo.

**Ensaiar a demonstração ao vivo:** abrir o jogo, rodar o cenário 3 com BFS, depois com A*, e
explicar em voz alta por que os caminhos diferem. É a demonstração mais forte que temos.

---

## 5. Bônus: jogo educacional — *opcional, até +1,5 ponto*

**Só começar depois que 1 a 4 estiverem prontos.** Os pontos de bônus só são atribuídos se a
implementação básica estiver funcionando corretamente.

Público-alvo definido pelo enunciado: **alunos com deficiência intelectual e crianças do Ensino
Fundamental**. Isso muda o critério de qualidade — não é "mais bonito", é *mais compreensível*.

| Recurso | Pontos |
|---|---|
| Transformação em jogo educacional completo | até 0,5 |
| Animações e recursos de interação | até 0,3 |
| Fases, missões ou níveis adicionais | até 0,2 |
| Geração automática / editor de cenários | até 0,2 |
| Outros recursos relevantes | até 0,3 |

Diretrizes do enunciado para esse público: clareza das instruções, simplicidade da interface,
facilidade de interação, legibilidade dos elementos visuais e apresentação objetiva das
informações educativas.

---

## 6. Antes de entregar — *checklist de postagem*

- [ ] Adicionar os nomes de todos os integrantes no README e no relatório.
- [ ] Conferir se os nomes da equipe foram lançados no arquivo compartilhado no Drive
      (prazo era **16/09/2026** — verificar se já foi feito).
- [ ] Compactar em `.zip` ou `.rar`: código-fonte + executável/dependências + relatório técnico.
- [ ] Postar no Moodle até **02/10/2026**. **Apenas 1 integrante posta.**
- [ ] Lembrete: faltar código *ou* relatório conta como não entrega do trabalho.
