"""Registro das metricas das execucoes e exportacao para CSV."""

import csv
from dataclasses import dataclass, asdict
from pathlib import Path

CAMPOS = [
    "cenario",
    "foco",
    "metodo",
    "sucesso",
    "passos",
    "custo",
    "tempo_s",
    "estados_expandidos",
    "estados_gerados",
    "fronteira_maxima",
]


@dataclass
class Registro:
    cenario: str
    foco: str
    metodo: str
    sucesso: bool
    passos: int
    custo: int
    tempo_s: float
    estados_expandidos: int | str = "-"
    estados_gerados: int | str = "-"
    fronteira_maxima: int | str = "-"


def exportar_csv(registros: list[Registro], destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS)
        escritor.writeheader()
        for registro in registros:
            escritor.writerow(asdict(registro))
    return destino


def anexar_csv(registro: Registro, destino: Path) -> Path:
    """Acrescenta um registro ao CSV, criando o cabecalho se o arquivo ainda nao existir."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    novo = not destino.exists()
    with destino.open("a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS)
        if novo:
            escritor.writeheader()
        escritor.writerow(asdict(registro))
    return destino


def tabela_texto(registros: list[Registro]) -> str:
    """Formata os registros como tabela de largura fixa, util para o relatorio."""
    cabecalho = [
        "Cenario", "Foco", "Metodo", "Passos", "Custo",
        "Tempo(s)", "Expandidos", "Gerados", "Fronteira",
    ]
    linhas = [
        [
            r.cenario, r.foco, r.metodo, str(r.passos), str(r.custo),
            f"{r.tempo_s:.6f}", str(r.estados_expandidos),
            str(r.estados_gerados), str(r.fronteira_maxima),
        ]
        for r in registros
    ]

    larguras = [
        max(len(cabecalho[i]), max((len(l[i]) for l in linhas), default=0))
        for i in range(len(cabecalho))
    ]
    separador = "-+-".join("-" * w for w in larguras)
    saida = [" | ".join(c.ljust(larguras[i]) for i, c in enumerate(cabecalho)), separador]
    saida.extend(" | ".join(c.ljust(larguras[i]) for i, c in enumerate(l)) for l in linhas)
    return "\n".join(saida)
