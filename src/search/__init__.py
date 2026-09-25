"""Algoritmos de busca implementados para o projeto."""

from src.search.astar import a_estrela
from src.search.bfs import bfs
from src.search.dfs import dfs
from src.search.greedy import busca_gulosa

ALGORITMOS = {
    "BFS": bfs,
    "DFS": dfs,
    "Gulosa": busca_gulosa,
    "A*": a_estrela,
}

__all__ = ["ALGORITMOS", "bfs", "dfs", "busca_gulosa", "a_estrela"]
