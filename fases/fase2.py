import pygame
from config import *
from personagens.coelho import Coelho
from moedas import Moeda
from obstaculos import Obstaculo
from personagens.inimigos import Inimigo

# Configurações iniciais
LARGURA_TELA = 800
ALTURA_TELA = 600
VERDE = (34, 177, 76)
PRETO = (0, 0, 0)
BLOCO_PRETO = (0, 0, 0)

# Redimensiona o fundo para o tamanho da tela
FUNDO = pygame.image.load('assets/imagens/fundoJogo.png')
FUNDO = pygame.transform.scale(FUNDO, (LARGURA_TELA, ALTURA_TELA))

class Fase2:
    def __init__(self, tela):
        self.tela = tela
        self.coelho = Coelho(100, ALTURA_TELA - 150)

        # Moedas
        self.moedas = [
            Moeda(250, ALTURA_TELA - 250),
            Moeda(600, ALTURA_TELA - 180),
            Moeda(450, ALTURA_TELA - 100)
        ]

        # Inimigos (com movimento)
        self.inimigos = [
            Inimigo(100, ALTURA_TELA - 150, "vertical", 100, 200),
            Inimigo(200, ALTURA_TELA - 150, "horizontal", 100, 300),
            Inimigo(450, ALTURA_TELA - 250, "vertical", 100, 400),
            Inimigo(600, ALTURA_TELA - 150, "horizontal", 500, 700),
        ]

        # Obstáculos (agora servem como plataformas e não causam dano)
        self.obstaculos = [
            Obstaculo(350, ALTURA_TELA - 180),  # Obstáculo 1
            Obstaculo(450, ALTURA_TELA - 220),  # Obstáculo 2
            Obstaculo(550, ALTURA_TELA - 250),  # Obstáculo 3
            Obstaculo(700, ALTURA_TELA - 150),  # Obstáculo 4
            Obstaculo(750, ALTURA_TELA - 100),  # Obstáculo 5
        ]

        # Bloco preto para indicar o fim da fase
        self.bloco_fim = pygame.Rect(LARGURA_TELA - 50, ALTURA_TELA - 250, 50, 50)

        self.fim_da_fase = False
        self.pontuacao = 0
        self.terminou_fase = False

    def desenhar(self):
        self.tela.blit(FUNDO, (0, 0))
        self.coelho.desenhar(self.tela)

        # Desenha as moedas
        for moeda in self.moedas:
            if not moeda.coletada:
                moeda.desenhar(self.tela)

        # Desenha os obstáculos
        for obstaculo in self.obstaculos:
            obstaculo.desenhar(self.tela)

        # Desenha os inimigos
        for inimigo in self.inimigos:
            inimigo.desenhar(self.tela)

        # Desenha o bloco de fim de fase
        pygame.draw.rect(self.tela, BLOCO_PRETO, self.bloco_fim)

        # Exibe o número de moedas e vidas
        font = pygame.font.Font(None, 36)
        moedas_text = font.render(f'Moedas: {self.coelho.moedas}', True, PRETO)
        vidas_text = font.render(f'Vidas: {self.coelho.vidas}', True, PRETO)
        self.tela.blit(moedas_text, (10, 10))
        self.tela.blit(vidas_text, (10, 40))

        if self.terminou_fase:
            font_end = pygame.font.Font(None, 48)
            mensagem = font_end.render("Você terminou a fase! Pressione Enter para continuar", True, (255, 255, 255))
            self.tela.blit(mensagem, (LARGURA_TELA / 2 - mensagem.get_width() / 2, ALTURA_TELA / 2))

    def atualizar(self):
        self.coelho.atualizar()

        # Verifica coleta de moedas
        for moeda in self.moedas:
            self.coelho.coletar_moeda(moeda)

        # Movimenta e verifica colisões com inimigos
        for inimigo in self.inimigos:
            inimigo.mover()
            if self.coelho.rect.colliderect(inimigo.rect):
                self.coelho.perder_vida()

                if self.coelho.vidas <= 0:
                    print("Game Over!")
                    pygame.quit()
                    exit()

        # Não há colisão com obstáculos agora, apenas plataformas
        for obstaculo in self.obstaculos:
            if self.coelho.rect.colliderect(obstaculo.rect):
                # Verifica se o coelho está em cima do obstáculo para subir nele
                if self.coelho.rect.bottom <= obstaculo.rect.top + 10:  # Ajuste para permitir o "pulo"
                    self.coelho.rect.y = obstaculo.rect.top - self.coelho.rect.height
                    self.coelho.vel_y = 0  # Impede que o personagem caia através do obstáculo

        # Verifica o bloco de fim de fase
        if self.coelho.rect.colliderect(self.bloco_fim):
            self.fim_da_fase = True
            self.terminou_fase = True

    def rodar(self):
        self.desenhar()
        self.atualizar()

        if self.fim_da_fase and self.terminou_fase:
            return "fase_3"  # Se a fase for concluída, vai para a fase 3
        return None
