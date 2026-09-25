# O que testar

## Já testado e aprovado

### Algoritmos
- [x] Os 4 algoritmos encontram solução nos 3 cenários, para **todos** os focos (não só o padrão).
- [x] A* devolve o menor custo em todos os casos testados.
- [x] BFS devolve o menor número de passos em todos os casos testados.
- [x] Métricas coerentes: `estados_gerados >= estados_expandidos` em todas as execuções.
- [x] Desempate estável na fila de prioridade — sem `TypeError` ao comparar nós com mesmo `f(n)`.

### Cenários
- [x] Todos os mapas têm linhas de largura uniforme.
- [x] Posição inicial de cada cenário é transitável.
- [x] Todos os focos são transitáveis e alcançáveis a partir da posição inicial.
- [x] Cenário 3 demonstra menos passos ≠ menor custo (BFS 17/68 vs A* 23/38).

### Interface
- [x] Menu renderiza e navega entre cenários, focos e algoritmos.
- [x] Troca de cenário reseta o índice do foco (evita índice inválido).
- [x] Jogo renderiza nas 3 escalas de mapa (8×10, 12×15, 16×20).
- [x] Todas as 12 combinações cenário × algoritmo renderizam sem erro.
- [x] Movimento do usuário bloqueado contra obstáculos e contra as bordas do mapa.
- [x] Alternância da exibição de estados explorados (tecla `E`).
- [x] Tela de resultados renderiza corretamente.
- [x] Execução manual é gravada em `results/execucoes_usuario.csv`.
- [x] Cores de usuário (azul), agente (vermelho) e explorados (lilás) são distinguíveis.

> Os testes acima foram feitos de forma automatizada, com o Pygame em modo headless.

---

## Ainda precisa ser testado

### Teste manual obrigatório — *ninguém jogou o jogo ainda de verdade*
- [ ] Abrir `python main.py` numa máquina real e jogar os 3 cenários do começo ao fim.
- [ ] Confirmar que a velocidade de animação do agente é confortável
      (`INTERVALO_AGENTE_MS = 180` em `src/ui.py` — ajustar se estiver rápido ou lento demais).
- [ ] Confirmar que a janela de 1180×720 cabe na tela usada na apresentação.
- [ ] Verificar se as fontes carregam (usa `segoeui`; em Linux pode cair para fallback).
- [ ] Confirmar que a missão só termina quando **ambos** chegam, inclusive quando o
      usuário chega primeiro e fica esperando o agente.
- [ ] Testar a tecla `R` (reiniciar) no meio de uma missão.
- [ ] Testar `ESC` para voltar ao menu no meio de uma missão.

### Casos de borda ainda não exercitados
- [ ] Iniciar uma missão e **não** se mover — o agente termina sozinho e a missão fica
      aguardando o usuário? (Comportamento esperado: sim, fica aguardando.)
- [ ] Segurar uma tecla de movimento — o movimento repete ou exige toques separados?
      (Hoje só responde a `KEYDOWN`, ou seja, um passo por toque. Verificar se é confortável.)
- [ ] Fechar a janela no meio da missão (botão X) — encerra limpo?

### Antes da apresentação
- [ ] Rodar o projeto na máquina que será usada na sala de aula.
- [ ] Testar com o projetor: as cores dos terrenos continuam distinguíveis?
- [ ] Ter o `results/` já populado, caso não dê tempo de rodar tudo ao vivo.

---

## Como rodar a verificação automática

Não há suíte de testes formal no repositório. A verificação foi feita por scripts temporários.
Se quiser recriar uma checagem rápida de sanidade:

```python
from src.scenarios import CENARIOS
from src.search import ALGORITMOS

for cen in CENARIOS:
    grid = cen.construir()
    for foco in cen.focos:
        for nome, alg in ALGORITMOS.items():
            r = alg(grid, cen.inicio, foco.posicao)
            assert r.sucesso, (cen.nome, foco.tipo, nome)
            assert grid.custo_do_caminho(r.caminho) == r.custo
            print(cen.nome, foco.tipo, nome, r.passos, r.custo)
```

**Ideia para depois:** transformar isso num `testes.py` de verdade. Não é exigido pelo
enunciado, mas ajuda a não quebrar nada ao mexer no código perto da entrega.
