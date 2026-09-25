"""Cenarios do ambiente, em tres niveis de complexidade.

Legenda dos mapas:
    '.'  caminho livre / calcada (custo 1)
    'g'  grama (custo 2)
    'd'  terreno de dificil acesso (custo 4)
    '#'  obstaculo (intransponivel)
"""

from dataclasses import dataclass

from src.grid import Foco, Grid


@dataclass
class Cenario:
    nome: str
    descricao: str
    mapa: list[str]
    inicio: tuple[int, int]
    focos: list[Foco]
    foco_padrao: int = 0

    def construir(self) -> Grid:
        return Grid.de_mapa(self.mapa, self.inicio, self.focos)

    @property
    def objetivo(self) -> tuple[int, int]:
        return self.focos[self.foco_padrao].posicao


CENARIO_1 = Cenario(
    nome="Cenario 1 - Simples",
    descricao=(
        "Quintal pequeno, poucos obstaculos e poucos caminhos alternativos. "
        "Custos predominantemente uniformes."
    ),
    mapa=[
        "..........",
        "..##......",
        "..##..gg..",
        "......gg..",
        "....##....",
        "....##....",
        "..........",
        "..........",
    ],
    inicio=(0, 0),
    focos=[
        Foco(posicao=(7, 9), tipo="pneu"),
        Foco(posicao=(0, 8), tipo="vaso"),
    ],
)

CENARIO_2 = Cenario(
    nome="Cenario 2 - Intermediario",
    descricao=(
        "Conjunto de residencias com mais obstaculos e diferentes possibilidades "
        "de caminho ate o foco, que fica em um patio interno."
    ),
    mapa=[
        "...............",
        ".####.....####.",
        ".#...........#.",
        ".#.####.####.#.",
        "...#gg...gg#...",
        "...#.......#...",
        "...#.##.##.#...",
        ".....#...#.....",
        ".###.#...#.###.",
        ".....#####.....",
        "..gg.......gg..",
        "...............",
    ],
    inicio=(0, 0),
    focos=[
        Foco(posicao=(5, 7), tipo="caixa_dagua"),
        Foco(posicao=(11, 14), tipo="calha"),
        Foco(posicao=(10, 2), tipo="balde"),
    ],
)

CENARIO_3 = Cenario(
    nome="Cenario 3 - Complexo",
    descricao=(
        "Pequeno bairro com multiplos caminhos, obstaculos e uma faixa central de "
        "terreno de dificil acesso. O caminho com menor quantidade de passos "
        "atravessa a faixa cara; o caminho de menor custo contorna por cima, "
        "usando mais passos."
    ),
    mapa=[
        "....................",
        "..........g.........",
        "...####.....####....",
        "...####.....####....",
        "....................",
        "....................",
        "dddddddddddddddddddd",
        "ddddd####dddd###dddd",
        "dddddddddddddddddddd",
        "dddd###ddddddd##dddd",
        "dddddddddddddddddddd",
        "....................",
        "...ggg......ggg.....",
        "....####.....####...",
        "....................",
        "....................",
    ],
    inicio=(8, 1),
    focos=[
        Foco(posicao=(8, 18), tipo="piscina"),
        Foco(posicao=(0, 19), tipo="garrafa"),
        Foco(posicao=(15, 0), tipo="lixo"),
    ],
)

CENARIOS = [CENARIO_1, CENARIO_2, CENARIO_3]
