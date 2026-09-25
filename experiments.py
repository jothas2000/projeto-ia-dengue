"""Executa as 12 execucoes algoritmicas (3 cenarios x 4 algoritmos) sem interface grafica.

As 3 execucoes humanas sao registradas pelo jogo (main.py) em results/execucoes_usuario.csv.

Uso:
    python experiments.py
    python experiments.py --repeticoes 30    # media de tempo mais estavel
"""

import argparse
import statistics
from pathlib import Path

from src.metrics import Registro, exportar_csv, tabela_texto
from src.scenarios import CENARIOS
from src.search import ALGORITMOS

DESTINO = Path("results") / "execucoes_algoritmos.csv"


def executar(repeticoes: int) -> list[Registro]:
    registros: list[Registro] = []

    for cenario in CENARIOS:
        grid = cenario.construir()
        foco = cenario.focos[cenario.foco_padrao]

        for nome, algoritmo in ALGORITMOS.items():
            # O resultado e identico entre repeticoes; elas servem apenas para
            # estabilizar a medicao de tempo, sensivel a ruido do sistema.
            tempos = []
            resultado = None
            for _ in range(repeticoes):
                resultado = algoritmo(grid, cenario.inicio, foco.posicao)
                tempos.append(resultado.tempo)

            registros.append(
                Registro(
                    cenario=cenario.nome,
                    foco=f"{foco.tipo} {foco.posicao}",
                    metodo=nome,
                    sucesso=resultado.sucesso,
                    passos=resultado.passos,
                    custo=resultado.custo,
                    tempo_s=statistics.median(tempos),
                    estados_expandidos=resultado.estados_expandidos,
                    estados_gerados=resultado.estados_gerados,
                    fronteira_maxima=resultado.fronteira_maxima,
                )
            )

    return registros


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeticoes", type=int, default=15)
    args = parser.parse_args()

    registros = executar(args.repeticoes)
    print(tabela_texto(registros))
    caminho = exportar_csv(registros, DESTINO)
    print(f"\nResultados salvos em: {caminho}")


if __name__ == "__main__":
    main()
