"""Representacao do ambiente: matriz bidimensional de celulas com custos de deslocamento."""

from dataclasses import dataclass, field

LIVRE = "livre"
GRAMA = "grama"
DIFICIL = "dificil"
OBSTACULO = "obstaculo"

CUSTOS = {
    LIVRE: 1,
    GRAMA: 2,
    DIFICIL: 4,
}

CUSTO_MINIMO = min(CUSTOS.values())

SIMBOLOS = {
    ".": LIVRE,
    "g": GRAMA,
    "d": DIFICIL,
    "#": OBSTACULO,
}

# Ordem fixa de expansao (cima, baixo, esquerda, direita) para resultados reproduziveis.
ACOES = (
    ("cima", (-1, 0)),
    ("baixo", (1, 0)),
    ("esquerda", (0, -1)),
    ("direita", (0, 1)),
)


@dataclass
class Foco:
    """Foco de proliferacao posicionado sobre uma celula transitavel."""

    posicao: tuple[int, int]
    tipo: str


@dataclass
class Grid:
    """Ambiente do problema de busca.

    A matriz e tratada como um grafo implicito: os sucessores de uma posicao sao
    gerados sob demanda por `sucessores`, sem construcao previa de nos e arestas.
    """

    terreno: list[list[str]]
    inicio: tuple[int, int]
    focos: list[Foco] = field(default_factory=list)

    @property
    def linhas(self) -> int:
        return len(self.terreno)

    @property
    def colunas(self) -> int:
        return len(self.terreno[0])

    @classmethod
    def de_mapa(cls, mapa: list[str], inicio: tuple[int, int], focos: list[Foco]) -> "Grid":
        terreno = [[SIMBOLOS[c] for c in linha] for linha in mapa]
        return cls(terreno=terreno, inicio=inicio, focos=focos)

    def tipo(self, posicao: tuple[int, int]) -> str:
        linha, coluna = posicao
        return self.terreno[linha][coluna]

    def dentro(self, posicao: tuple[int, int]) -> bool:
        linha, coluna = posicao
        return 0 <= linha < self.linhas and 0 <= coluna < self.colunas

    def transitavel(self, posicao: tuple[int, int]) -> bool:
        return self.dentro(posicao) and self.tipo(posicao) != OBSTACULO

    def custo(self, posicao: tuple[int, int]) -> int:
        """Custo de entrar na celula indicada."""
        return CUSTOS[self.tipo(posicao)]

    def sucessores(self, posicao: tuple[int, int]) -> list[tuple[str, tuple[int, int], int]]:
        """Funcao sucessora: acoes validas a partir de `posicao`.

        Retorna triplas (acao, posicao_destino, custo_do_movimento).
        """
        linha, coluna = posicao
        resultado = []
        for acao, (dl, dc) in ACOES:
            destino = (linha + dl, coluna + dc)
            if self.transitavel(destino):
                resultado.append((acao, destino, self.custo(destino)))
        return resultado

    def foco_em(self, posicao: tuple[int, int]) -> Foco | None:
        for foco in self.focos:
            if foco.posicao == posicao:
                return foco
        return None

    def custo_do_caminho(self, caminho: list[tuple[int, int]]) -> int:
        """Soma dos custos das celulas percorridas, excluindo a posicao inicial."""
        return sum(self.custo(posicao) for posicao in caminho[1:])
