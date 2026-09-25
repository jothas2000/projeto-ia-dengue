"""Busca A*: combina custo acumulado e estimativa restante, f(n) = g(n) + h(n)."""

import heapq
import time

from src.grid import Grid
from src.node import No, ResultadoBusca
from src.search.heuristics import heuristica


def a_estrela(grid: Grid, inicio: tuple[int, int], objetivo: tuple[int, int]) -> ResultadoBusca:
    comeco = time.perf_counter()

    contador = 0
    raiz = No(estado=inicio)
    fronteira = [(heuristica(inicio, objetivo), contador, raiz)]
    melhor_g = {inicio: 0}
    visitados: set[tuple[int, int]] = set()
    expandidos = 0
    gerados = 1
    fronteira_maxima = 1
    ordem: list[tuple[int, int]] = []

    while fronteira:
        _, _, no = heapq.heappop(fronteira)
        if no.estado in visitados:
            continue

        visitados.add(no.estado)
        expandidos += 1
        ordem.append(no.estado)

        if no.estado == objetivo:
            caminho = no.caminho()
            return ResultadoBusca(
                algoritmo="A*",
                sucesso=True,
                caminho=caminho,
                custo=no.g,
                passos=len(caminho) - 1,
                estados_expandidos=expandidos,
                estados_gerados=gerados,
                fronteira_maxima=fronteira_maxima,
                tempo=time.perf_counter() - comeco,
                ordem_exploracao=ordem,
            )

        for acao, destino, custo in grid.sucessores(no.estado):
            if destino in visitados:
                continue
            novo_g = no.g + custo
            if destino in melhor_g and novo_g >= melhor_g[destino]:
                continue

            melhor_g[destino] = novo_g
            filho = no.filho(acao, destino, custo)
            contador += 1
            heapq.heappush(
                fronteira,
                (novo_g + heuristica(destino, objetivo), contador, filho),
            )
            gerados += 1

        fronteira_maxima = max(fronteira_maxima, len(fronteira))

    return ResultadoBusca(
        algoritmo="A*",
        sucesso=False,
        estados_expandidos=expandidos,
        estados_gerados=gerados,
        fronteira_maxima=fronteira_maxima,
        tempo=time.perf_counter() - comeco,
        ordem_exploracao=ordem,
    )
