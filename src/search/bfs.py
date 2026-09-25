"""Busca em Largura (BFS): explora o espaco de estados por niveis, usando fila FIFO."""

import time
from collections import deque

from src.grid import Grid
from src.node import No, ResultadoBusca


def bfs(grid: Grid, inicio: tuple[int, int], objetivo: tuple[int, int]) -> ResultadoBusca:
    comeco = time.perf_counter()

    raiz = No(estado=inicio)
    if inicio == objetivo:
        return ResultadoBusca(
            algoritmo="BFS",
            sucesso=True,
            caminho=[inicio],
            tempo=time.perf_counter() - comeco,
            estados_gerados=1,
            fronteira_maxima=1,
            ordem_exploracao=[inicio],
        )

    fronteira = deque([raiz])
    # Teste de objetivo na geracao: BFS nao precisa expandir o no objetivo.
    alcancados = {inicio}
    expandidos = 0
    gerados = 1
    fronteira_maxima = 1
    ordem: list[tuple[int, int]] = []

    while fronteira:
        no = fronteira.popleft()
        expandidos += 1
        ordem.append(no.estado)

        for acao, destino, custo in grid.sucessores(no.estado):
            if destino in alcancados:
                continue
            filho = no.filho(acao, destino, custo)
            gerados += 1

            if destino == objetivo:
                caminho = filho.caminho()
                return ResultadoBusca(
                    algoritmo="BFS",
                    sucesso=True,
                    caminho=caminho,
                    custo=filho.g,
                    passos=len(caminho) - 1,
                    estados_expandidos=expandidos,
                    estados_gerados=gerados,
                    fronteira_maxima=fronteira_maxima,
                    tempo=time.perf_counter() - comeco,
                    ordem_exploracao=ordem,
                )

            alcancados.add(destino)
            fronteira.append(filho)

        fronteira_maxima = max(fronteira_maxima, len(fronteira))

    return ResultadoBusca(
        algoritmo="BFS",
        sucesso=False,
        estados_expandidos=expandidos,
        estados_gerados=gerados,
        fronteira_maxima=fronteira_maxima,
        tempo=time.perf_counter() - comeco,
        ordem_exploracao=ordem,
    )
