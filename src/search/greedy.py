"""Busca Gulosa: ordena a fronteira apenas pela estimativa heuristica f(n) = h(n)."""

import heapq
import time

from src.grid import Grid
from src.node import No, ResultadoBusca
from src.search.heuristics import heuristica


def busca_gulosa(grid: Grid, inicio: tuple[int, int], objetivo: tuple[int, int]) -> ResultadoBusca:
    comeco = time.perf_counter()

    contador = 0  # desempate estavel: preserva a ordem de insercao entre f(n) iguais
    fronteira = [(heuristica(inicio, objetivo), contador, No(estado=inicio))]
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
                algoritmo="Gulosa",
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
            contador += 1
            filho = no.filho(acao, destino, custo)
            heapq.heappush(fronteira, (heuristica(destino, objetivo), contador, filho))
            gerados += 1

        fronteira_maxima = max(fronteira_maxima, len(fronteira))

    return ResultadoBusca(
        algoritmo="Gulosa",
        sucesso=False,
        estados_expandidos=expandidos,
        estados_gerados=gerados,
        fronteira_maxima=fronteira_maxima,
        tempo=time.perf_counter() - comeco,
        ordem_exploracao=ordem,
    )
