"""No da arvore de busca e estruturas de resultado compartilhadas pelos algoritmos."""

from dataclasses import dataclass, field


@dataclass
class No:
    """No da arvore de busca.

    `g` acumula o custo real desde o estado inicial; `pai` permite reconstruir o caminho.
    """

    estado: tuple[int, int]
    pai: "No | None" = None
    acao: str | None = None
    g: int = 0
    profundidade: int = 0

    def filho(self, acao: str, estado: tuple[int, int], custo: int) -> "No":
        return No(
            estado=estado,
            pai=self,
            acao=acao,
            g=self.g + custo,
            profundidade=self.profundidade + 1,
        )

    def caminho(self) -> list[tuple[int, int]]:
        """Reconstroi o caminho da raiz ate este no."""
        sequencia = []
        atual: No | None = self
        while atual is not None:
            sequencia.append(atual.estado)
            atual = atual.pai
        sequencia.reverse()
        return sequencia


@dataclass
class ResultadoBusca:
    """Metricas e saida de uma execucao de algoritmo de busca."""

    algoritmo: str
    sucesso: bool
    caminho: list[tuple[int, int]] = field(default_factory=list)
    custo: int = 0
    passos: int = 0
    estados_expandidos: int = 0
    estados_gerados: int = 0
    fronteira_maxima: int = 0
    tempo: float = 0.0
    ordem_exploracao: list[tuple[int, int]] = field(default_factory=list)
