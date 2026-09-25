"""Conteudo educacional associado a cada tipo de foco de proliferacao.

Informacoes baseadas nas orientacoes de prevencao do Ministerio da Saude e da
Fundacao Oswaldo Cruz (Fiocruz). Fontes completas listadas no relatorio tecnico.
"""

MENSAGENS = {
    "pneu": (
        "Pneu com agua acumulada",
        "Pneus expostos acumulam agua da chuva e favorecem a proliferacao do mosquito. "
        "Guarde-os em local coberto, fure-os para escoar a agua ou encaminhe para "
        "destinacao adequada.",
    ),
    "vaso": (
        "Prato de vaso de planta",
        "Pratos sob vasos retem agua parada. Elimine o prato, preencha-o com areia ate "
        "a borda ou lave-o com escova e sabao uma vez por semana.",
    ),
    "garrafa": (
        "Garrafa destampada",
        "Garrafas deixadas de boca para cima juntam agua. Guarde-as sempre com a boca "
        "voltada para baixo e mantenha-as em local coberto.",
    ),
    "balde": (
        "Balde descoberto",
        "Baldes e bacias devem ser guardados virados para baixo, sem acumular agua. "
        "Quando em uso, mantenha-os sempre tampados.",
    ),
    "caixa_dagua": (
        "Caixa-d'agua mal vedada",
        "A caixa-d'agua precisa de tampa firme e bem vedada. Verifique periodicamente "
        "se nao ha frestas por onde o mosquito possa entrar para depositar ovos.",
    ),
    "calha": (
        "Calha entupida",
        "Folhas e sujeira entopem calhas e retem agua. Limpe-as regularmente para "
        "garantir o escoamento e evitar criadouros no telhado.",
    ),
    "ralo": (
        "Ralo sem uso frequente",
        "Ralos pouco utilizados acumulam agua no sifao. Mantenha-os fechados com tampa "
        "ou tela e jogue agua sanitaria semanalmente.",
    ),
    "lixo": (
        "Lixo a ceu aberto",
        "Embalagens e recipientes descartados acumulam agua da chuva. Mantenha o lixo "
        "em sacos fechados e as lixeiras sempre tampadas.",
    ),
    "piscina": (
        "Piscina sem tratamento",
        "Piscinas paradas sem cloro viram criadouro. Mantenha o tratamento em dia ou "
        "cubra a piscina quando estiver fora de uso.",
    ),
    "bebedouro": (
        "Bebedouro de animais",
        "Bebedouros de animais devem ser lavados com escova e trocados diariamente, "
        "pois a agua parada por poucos dias ja permite o desenvolvimento das larvas.",
    ),
}


def mensagem(tipo_foco: str) -> tuple[str, str]:
    """Retorna (titulo, orientacao) para o tipo de foco informado."""
    return MENSAGENS.get(
        tipo_foco,
        ("Foco de dengue", "Elimine qualquer recipiente que possa acumular agua parada."),
    )
