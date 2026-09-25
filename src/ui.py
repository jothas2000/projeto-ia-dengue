"""Interface grafica do ambiente de simulacao (Pygame)."""

import time
from pathlib import Path

import pygame

from src.educational import mensagem
from src.grid import DIFICIL, GRAMA, LIVRE, OBSTACULO
from src.metrics import Registro, anexar_csv
from src.scenarios import CENARIOS
from src.search import ALGORITMOS

LARGURA, ALTURA = 1180, 720
PAINEL = 360
MARGEM = 20
INTERVALO_AGENTE_MS = 180

CSV_USUARIO = Path("results") / "execucoes_usuario.csv"

COR_FUNDO = (248, 249, 251)
COR_PAINEL = (255, 255, 255)
COR_BORDA = (214, 219, 227)
COR_TEXTO = (32, 38, 48)
COR_TEXTO_FRACO = (112, 122, 138)
COR_DESTAQUE = (23, 106, 201)

CORES_TERRENO = {
    LIVRE: (240, 242, 245),
    GRAMA: (178, 219, 168),
    DIFICIL: (206, 174, 132),
    OBSTACULO: (84, 92, 104),
}

COR_EXPLORADO = (206, 196, 240)
COR_CAMINHO_AGENTE = (236, 138, 120)
COR_CAMINHO_USUARIO = (86, 148, 228)
COR_USUARIO = (23, 106, 201)
COR_AGENTE = (201, 58, 42)
COR_FOCO = (222, 164, 34)
COR_OBJETIVO = (196, 52, 118)

TECLAS_MOVIMENTO = {
    pygame.K_UP: (-1, 0), pygame.K_w: (-1, 0),
    pygame.K_DOWN: (1, 0), pygame.K_s: (1, 0),
    pygame.K_LEFT: (0, -1), pygame.K_a: (0, -1),
    pygame.K_RIGHT: (0, 1), pygame.K_d: (0, 1),
}

MENU, JOGO, RESULTADOS = "menu", "jogo", "resultados"


class Jogo:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Agente de Combate a Dengue - UTFPR")
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.relogio = pygame.time.Clock()

        self.fonte_titulo = pygame.font.SysFont("segoeui", 30, bold=True)
        self.fonte_sub = pygame.font.SysFont("segoeui", 20, bold=True)
        self.fonte = pygame.font.SysFont("segoeui", 17)
        self.fonte_peq = pygame.font.SysFont("segoeui", 14)

        self.estado = MENU
        self.indice_cenario = 0
        self.indice_foco = 0
        self.indice_algoritmo = 0
        self.item_menu = 0
        self.mostrar_explorados = True
        self.rodando = True

    # ------------------------------------------------------------------ menu

    @property
    def cenario(self):
        return CENARIOS[self.indice_cenario]

    @property
    def foco(self):
        return self.cenario.focos[self.indice_foco]

    @property
    def nome_algoritmo(self) -> str:
        return list(ALGORITMOS)[self.indice_algoritmo]

    def opcoes_menu(self) -> list[tuple[str, str]]:
        return [
            ("Cenario", self.cenario.nome),
            ("Foco de dengue", f"{self.foco.tipo} {self.foco.posicao}"),
            ("Algoritmo do agente", self.nome_algoritmo),
        ]

    def ajustar_opcao(self, delta: int) -> None:
        if self.item_menu == 0:
            self.indice_cenario = (self.indice_cenario + delta) % len(CENARIOS)
            self.indice_foco = 0
        elif self.item_menu == 1:
            self.indice_foco = (self.indice_foco + delta) % len(self.cenario.focos)
        else:
            self.indice_algoritmo = (self.indice_algoritmo + delta) % len(ALGORITMOS)

    # --------------------------------------------------------------- missao

    def iniciar_missao(self) -> None:
        """Prepara a missao: o agente resolve a busca imediatamente e o tempo do
        algoritmo e registrado separadamente do tempo de animacao, conforme 2.4.3."""
        self.grid = self.cenario.construir()
        self.objetivo = self.foco.posicao
        self.resultado = ALGORITMOS[self.nome_algoritmo](
            self.grid, self.cenario.inicio, self.objetivo
        )

        self.pos_usuario = self.cenario.inicio
        self.caminho_usuario = [self.cenario.inicio]
        self.custo_usuario = 0
        self.passos_usuario = 0
        self.usuario_concluiu = False
        self.tempo_usuario = 0.0

        self.indice_agente = 0
        self.agente_concluiu = not self.resultado.sucesso
        self.proximo_passo_agente = pygame.time.get_ticks() + INTERVALO_AGENTE_MS

        self.inicio_missao = time.perf_counter()
        self.registrado = False
        self.estado = JOGO

    def pos_agente(self) -> tuple[int, int]:
        if not self.resultado.sucesso:
            return self.cenario.inicio
        return self.resultado.caminho[self.indice_agente]

    def mover_usuario(self, delta: tuple[int, int]) -> None:
        if self.usuario_concluiu:
            return
        destino = (self.pos_usuario[0] + delta[0], self.pos_usuario[1] + delta[1])
        if not self.grid.transitavel(destino):
            return

        self.pos_usuario = destino
        self.caminho_usuario.append(destino)
        self.custo_usuario += self.grid.custo(destino)
        self.passos_usuario += 1

        if destino == self.objetivo:
            self.usuario_concluiu = True
            self.tempo_usuario = time.perf_counter() - self.inicio_missao

    def atualizar_agente(self) -> None:
        if self.agente_concluiu:
            return
        agora = pygame.time.get_ticks()
        if agora < self.proximo_passo_agente:
            return

        self.proximo_passo_agente = agora + INTERVALO_AGENTE_MS
        if self.indice_agente + 1 < len(self.resultado.caminho):
            self.indice_agente += 1
        else:
            self.agente_concluiu = True

    def registrar_execucao(self) -> None:
        """Grava a execucao manual do usuario para compor a analise experimental."""
        if self.registrado:
            return
        self.registrado = True
        anexar_csv(
            Registro(
                cenario=self.cenario.nome,
                foco=f"{self.foco.tipo} {self.foco.posicao}",
                metodo="Usuario",
                sucesso=self.usuario_concluiu,
                passos=self.passos_usuario,
                custo=self.custo_usuario,
                tempo_s=self.tempo_usuario,
            ),
            CSV_USUARIO,
        )

    # -------------------------------------------------------------- desenho

    def geometria_grid(self) -> tuple[int, int, int]:
        largura_util = LARGURA - PAINEL - MARGEM * 3
        altura_util = ALTURA - MARGEM * 2 - 70
        lado = min(largura_util // self.grid.colunas, altura_util // self.grid.linhas)
        ox = MARGEM + (largura_util - lado * self.grid.colunas) // 2
        oy = MARGEM + 70 + (altura_util - lado * self.grid.linhas) // 2
        return ox, oy, lado

    def retangulo(self, posicao, ox, oy, lado) -> pygame.Rect:
        linha, coluna = posicao
        return pygame.Rect(ox + coluna * lado, oy + linha * lado, lado, lado)

    def desenhar_grid(self) -> None:
        ox, oy, lado = self.geometria_grid()

        for linha in range(self.grid.linhas):
            for coluna in range(self.grid.colunas):
                celula = (linha, coluna)
                rect = self.retangulo(celula, ox, oy, lado)
                pygame.draw.rect(self.tela, CORES_TERRENO[self.grid.tipo(celula)], rect)
                pygame.draw.rect(self.tela, (226, 230, 236), rect, 1)

        if self.mostrar_explorados:
            explorados = set(self.resultado.ordem_exploracao[: self.indice_agente_explorado()])
            for celula in explorados:
                rect = self.retangulo(celula, ox, oy, lado).inflate(-lado // 3, -lado // 3)
                pygame.draw.rect(self.tela, COR_EXPLORADO, rect, border_radius=3)

        for celula in self.caminho_usuario:
            rect = self.retangulo(celula, ox, oy, lado).inflate(-lado // 2, -lado // 2)
            pygame.draw.rect(self.tela, COR_CAMINHO_USUARIO, rect, border_radius=2)

        if self.resultado.sucesso:
            for celula in self.resultado.caminho[: self.indice_agente + 1]:
                rect = self.retangulo(celula, ox, oy, lado).inflate(-lado * 2 // 3, -lado * 2 // 3)
                pygame.draw.rect(self.tela, COR_CAMINHO_AGENTE, rect, border_radius=2)

        for foco in self.cenario.focos:
            rect = self.retangulo(foco.posicao, ox, oy, lado)
            cor = COR_OBJETIVO if foco.posicao == self.objetivo else COR_FOCO
            pygame.draw.circle(self.tela, cor, rect.center, lado // 2 - 3, 4)

        rect_inicio = self.retangulo(self.cenario.inicio, ox, oy, lado)
        pygame.draw.rect(self.tela, (150, 158, 172), rect_inicio, 2)

        rect_agente = self.retangulo(self.pos_agente(), ox, oy, lado)
        pygame.draw.circle(self.tela, COR_AGENTE, rect_agente.center, lado // 2 - 5)
        rect_usuario = self.retangulo(self.pos_usuario, ox, oy, lado)
        pygame.draw.circle(self.tela, COR_USUARIO, rect_usuario.center, lado // 2 - 5)

    def indice_agente_explorado(self) -> int:
        """Quantos estados explorados ja foram revelados, proporcional ao avanco do agente."""
        if not self.resultado.sucesso or len(self.resultado.caminho) <= 1:
            return len(self.resultado.ordem_exploracao)
        fracao = self.indice_agente / (len(self.resultado.caminho) - 1)
        return int(len(self.resultado.ordem_exploracao) * fracao)

    def texto(self, conteudo, fonte, cor, x, y) -> int:
        superficie = fonte.render(conteudo, True, cor)
        self.tela.blit(superficie, (x, y))
        return y + fonte.get_height()

    def desenhar_painel(self) -> None:
        x = LARGURA - PAINEL - MARGEM
        painel = pygame.Rect(x, MARGEM, PAINEL, ALTURA - MARGEM * 2)
        pygame.draw.rect(self.tela, COR_PAINEL, painel, border_radius=10)
        pygame.draw.rect(self.tela, COR_BORDA, painel, 1, border_radius=10)

        px, y = x + 18, MARGEM + 18
        y = self.texto("Missao em andamento", self.fonte_sub, COR_TEXTO, px, y) + 4
        y = self.texto(self.cenario.nome, self.fonte_peq, COR_TEXTO_FRACO, px, y)
        y = self.texto(
            f"Foco: {self.foco.tipo} {self.foco.posicao}", self.fonte_peq, COR_TEXTO_FRACO, px, y
        ) + 14

        y = self.texto("USUARIO", self.fonte_sub, COR_USUARIO, px, y) + 4
        for rotulo, valor in [
            ("Passos", self.passos_usuario),
            ("Custo acumulado", self.custo_usuario),
            ("Tempo", f"{self.tempo_decorrido_usuario():.1f} s"),
            ("Situacao", "Chegou ao foco" if self.usuario_concluiu else "Em deslocamento"),
        ]:
            y = self.texto(f"{rotulo}: {valor}", self.fonte, COR_TEXTO, px, y)
        y += 14

        y = self.texto(f"AGENTE - {self.nome_algoritmo}", self.fonte_sub, COR_AGENTE, px, y) + 4
        if self.resultado.sucesso:
            linhas = [
                ("Passos", self.resultado.passos),
                ("Custo total", self.resultado.custo),
                ("Estados expandidos", self.resultado.estados_expandidos),
                ("Estados gerados", self.resultado.estados_gerados),
                ("Fronteira maxima", self.resultado.fronteira_maxima),
                ("Tempo de busca", f"{self.resultado.tempo:.6f} s"),
                ("Situacao", "Chegou ao foco" if self.agente_concluiu else "Em deslocamento"),
            ]
        else:
            linhas = [("Situacao", "Sem solucao encontrada")]
        for rotulo, valor in linhas:
            y = self.texto(f"{rotulo}: {valor}", self.fonte, COR_TEXTO, px, y)

        y = ALTURA - MARGEM - 128
        y = self.texto("Controles", self.fonte_sub, COR_TEXTO, px, y) + 4
        for linha in [
            "Setas / WASD - mover o usuario",
            "E - mostrar ou ocultar estados explorados",
            "R - reiniciar a missao",
            "ESC - voltar ao menu",
        ]:
            y = self.texto(linha, self.fonte_peq, COR_TEXTO_FRACO, px, y)

    def tempo_decorrido_usuario(self) -> float:
        if self.usuario_concluiu:
            return self.tempo_usuario
        return time.perf_counter() - self.inicio_missao

    def desenhar_legenda(self) -> None:
        itens = [
            ("Livre (1)", CORES_TERRENO[LIVRE]),
            ("Grama (2)", CORES_TERRENO[GRAMA]),
            ("Dificil (4)", CORES_TERRENO[DIFICIL]),
            ("Obstaculo", CORES_TERRENO[OBSTACULO]),
            ("Explorado", COR_EXPLORADO),
            ("Usuario", COR_USUARIO),
            ("Agente", COR_AGENTE),
            ("Objetivo", COR_OBJETIVO),
        ]
        x, y = MARGEM, MARGEM + 34
        for rotulo, cor in itens:
            pygame.draw.rect(self.tela, cor, pygame.Rect(x, y + 3, 14, 14), border_radius=3)
            pygame.draw.rect(self.tela, COR_BORDA, pygame.Rect(x, y + 3, 14, 14), 1, border_radius=3)
            superficie = self.fonte_peq.render(rotulo, True, COR_TEXTO_FRACO)
            self.tela.blit(superficie, (x + 20, y))
            x += 22 + superficie.get_width() + 14

    def desenhar_menu(self) -> None:
        self.tela.fill(COR_FUNDO)
        x, y = MARGEM + 40, MARGEM + 40
        y = self.texto("Agente de Combate a Dengue", self.fonte_titulo, COR_TEXTO, x, y) + 6
        y = self.texto(
            "Usuario e agente inteligente resolvem a mesma missao no mesmo cenario.",
            self.fonte, COR_TEXTO_FRACO, x, y,
        ) + 34

        for indice, (rotulo, valor) in enumerate(self.opcoes_menu()):
            selecionado = indice == self.item_menu
            caixa = pygame.Rect(x, y, 640, 56)
            pygame.draw.rect(
                self.tela, (232, 240, 252) if selecionado else COR_PAINEL, caixa, border_radius=8
            )
            pygame.draw.rect(
                self.tela, COR_DESTAQUE if selecionado else COR_BORDA, caixa,
                2 if selecionado else 1, border_radius=8,
            )
            self.texto(rotulo, self.fonte_peq, COR_TEXTO_FRACO, x + 16, y + 8)
            self.texto(valor, self.fonte_sub, COR_TEXTO, x + 16, y + 26)
            self.texto("< >", self.fonte_sub, COR_TEXTO_FRACO, x + 600, y + 16)
            y += 68

        y += 14
        y = self.texto(self.cenario.descricao[:78], self.fonte_peq, COR_TEXTO_FRACO, x, y)
        if len(self.cenario.descricao) > 78:
            y = self.texto(self.cenario.descricao[78:156], self.fonte_peq, COR_TEXTO_FRACO, x, y)
        y += 24

        for linha in [
            "Setas cima/baixo - escolher a opcao",
            "Setas esquerda/direita - alterar o valor",
            "ENTER - iniciar a missao        ESC - sair",
        ]:
            y = self.texto(linha, self.fonte, COR_TEXTO_FRACO, x, y)

    def desenhar_resultados(self) -> None:
        self.tela.fill(COR_FUNDO)
        x, y = MARGEM + 40, MARGEM + 30
        y = self.texto("Resultado da missao", self.fonte_titulo, COR_TEXTO, x, y) + 4
        y = self.texto(
            f"{self.cenario.nome}  -  agente com {self.nome_algoritmo}",
            self.fonte, COR_TEXTO_FRACO, x, y,
        ) + 24

        titulo, orientacao = mensagem(self.foco.tipo)
        caixa = pygame.Rect(x, y, LARGURA - (MARGEM + 40) * 2, 96)
        pygame.draw.rect(self.tela, (255, 249, 230), caixa, border_radius=8)
        pygame.draw.rect(self.tela, (233, 206, 132), caixa, 1, border_radius=8)
        self.texto(titulo, self.fonte_sub, (138, 94, 12), x + 16, y + 12)
        linhas_texto = quebrar_texto(orientacao, self.fonte, caixa.width - 32)
        yy = y + 40
        for linha in linhas_texto:
            yy = self.texto(linha, self.fonte, (108, 78, 20), x + 16, yy)
        y += 120

        colunas = ["Metrica", "Usuario", f"Agente ({self.nome_algoritmo})"]
        dados = [
            ("Passos", str(self.passos_usuario), str(self.resultado.passos)),
            ("Custo total", str(self.custo_usuario), str(self.resultado.custo)),
            ("Tempo", f"{self.tempo_usuario:.2f} s", f"{self.resultado.tempo:.6f} s"),
            ("Estados expandidos", "-", str(self.resultado.estados_expandidos)),
            ("Estados gerados", "-", str(self.resultado.estados_gerados)),
            ("Fronteira maxima", "-", str(self.resultado.fronteira_maxima)),
        ]

        larguras = [300, 200, 240]
        for indice, titulo_coluna in enumerate(colunas):
            self.texto(titulo_coluna, self.fonte_sub, COR_TEXTO, x + sum(larguras[:indice]), y)
        y += 32
        for linha_dados in dados:
            for indice, celula in enumerate(linha_dados):
                cor = COR_TEXTO if indice == 0 else COR_TEXTO_FRACO
                self.texto(celula, self.fonte, cor, x + sum(larguras[:indice]), y)
            y += 26

        y += 20
        if self.custo_usuario < self.resultado.custo:
            veredito = "O usuario alcancou o foco com custo menor que o agente."
        elif self.custo_usuario == self.resultado.custo:
            veredito = "Usuario e agente alcancaram o foco com o mesmo custo."
        else:
            veredito = "O agente alcancou o foco com custo menor que o usuario."
        y = self.texto(veredito, self.fonte_sub, COR_DESTAQUE, x, y) + 24

        self.texto("ENTER - voltar ao menu      R - repetir a missao",
                   self.fonte, COR_TEXTO_FRACO, x, y)

    # ----------------------------------------------------------------- loop

    def processar_eventos(self) -> None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                self.processar_tecla(evento.key)

    def processar_tecla(self, tecla: int) -> None:
        if self.estado == MENU:
            if tecla == pygame.K_ESCAPE:
                self.rodando = False
            elif tecla in (pygame.K_UP, pygame.K_w):
                self.item_menu = (self.item_menu - 1) % 3
            elif tecla in (pygame.K_DOWN, pygame.K_s):
                self.item_menu = (self.item_menu + 1) % 3
            elif tecla in (pygame.K_LEFT, pygame.K_a):
                self.ajustar_opcao(-1)
            elif tecla in (pygame.K_RIGHT, pygame.K_d):
                self.ajustar_opcao(1)
            elif tecla in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self.iniciar_missao()

        elif self.estado == JOGO:
            if tecla == pygame.K_ESCAPE:
                self.estado = MENU
            elif tecla == pygame.K_r:
                self.iniciar_missao()
            elif tecla == pygame.K_e:
                self.mostrar_explorados = not self.mostrar_explorados
            elif tecla in TECLAS_MOVIMENTO:
                self.mover_usuario(TECLAS_MOVIMENTO[tecla])

        elif self.estado == RESULTADOS:
            if tecla == pygame.K_r:
                self.iniciar_missao()
            elif tecla in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_ESCAPE, pygame.K_SPACE):
                self.estado = MENU

    def executar(self) -> None:
        while self.rodando:
            self.processar_eventos()

            if self.estado == MENU:
                self.desenhar_menu()
            elif self.estado == JOGO:
                self.atualizar_agente()
                # A missao so termina quando ambos alcancam o foco (secao 2.4.3).
                if self.usuario_concluiu and self.agente_concluiu:
                    self.registrar_execucao()
                    self.estado = RESULTADOS
                else:
                    self.tela.fill(COR_FUNDO)
                    self.texto(self.cenario.nome, self.fonte_sub, COR_TEXTO, MARGEM, MARGEM)
                    self.desenhar_legenda()
                    self.desenhar_grid()
                    self.desenhar_painel()
            elif self.estado == RESULTADOS:
                self.desenhar_resultados()

            pygame.display.flip()
            self.relogio.tick(60)

        pygame.quit()


def quebrar_texto(texto: str, fonte: pygame.font.Font, largura: int) -> list[str]:
    palavras = texto.split()
    linhas, atual = [], ""
    for palavra in palavras:
        teste = f"{atual} {palavra}".strip()
        if fonte.size(teste)[0] <= largura:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas
