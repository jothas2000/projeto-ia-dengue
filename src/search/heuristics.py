"""Funcao heuristica usada pela Busca Gulosa e pelo A*."""

from src.grid import CUSTO_MINIMO


def manhattan(posicao: tuple[int, int], objetivo: tuple[int, int]) -> int:
    """Distancia Manhattan: numero minimo de movimentos ate o objetivo."""
    return abs(posicao[0] - objetivo[0]) + abs(posicao[1] - objetivo[1])


def heuristica(posicao: tuple[int, int], objetivo: tuple[int, int]) -> int:
    """Distancia Manhattan ponderada pelo custo minimo de um movimento.

    Como todo movimento custa ao menos CUSTO_MINIMO, o valor retornado nunca
    supera o custo real restante, o que mantem a heuristica admissivel e
    consistente mesmo com terrenos de custos distintos.
    """
    return manhattan(posicao, objetivo) * CUSTO_MINIMO
