"""Busca em Profundidade (DFS): aprofunda um ramo antes de explorar alternativas."""

import time

from src.grid import Grid
from src.node import No, ResultadoBusca


def dfs(grid: Grid, inicio: tuple[int, int], objetivo: tuple[int, int]) -> ResultadoBusca:
    comeco = time.perf_counter()

    fronteira = [No(estado=inicio)]
    visitados: set[tuple[int, int]] = set()
    expandidos = 0
    gerados = 1
    fronteira_maxima = 1
    ordem: list[tuple[int, int]] = []

    while fronteira:
        no = fronteira.pop()
        if no.estado in visitados:
            continue

        visitados.add(no.estado)
        expandidos += 1
        ordem.append(no.estado)

        if no.estado == objetivo:
            caminho = no.caminho()
            return ResultadoBusca(
                algoritmo="DFS",
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

        # Invertido para que a pilha desempilhe na mesma ordem de acoes da BFS.
        for acao, destino, custo in reversed(grid.sucessores(no.estado)):
            if destino in visitados:
                continue
            fronteira.append(no.filho(acao, destino, custo))
            gerados += 1

        fronteira_maxima = max(fronteira_maxima, len(fronteira))

    return ResultadoBusca(
        algoritmo="DFS",
        sucesso=False,
        estados_expandidos=expandidos,
        estados_gerados=gerados,
        fronteira_maxima=fronteira_maxima,
        tempo=time.perf_counter() - comeco,
        ordem_exploracao=ordem,
    )
