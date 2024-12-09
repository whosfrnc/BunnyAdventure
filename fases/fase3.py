import pygame
from config import *
from personagens.coelho import Coelho
from moedas import Moeda
from obstaculos import Obstaculo
from personagens.inimigos import Inimigo

# Configurações iniciais
LARGURA_TELA = 800
ALTURA_TELA = 600
PRETO = (0, 0, 0)
BLOCO_PRETO = (0, 0, 0)

# Redimensiona o fundo para o tamanho da tela
FUNDO = pygame.image.load('assets/imagens/fundoJogo.png')  # Pode ser um fundo diferente para a Fase 3
FUNDO = pygame.transform.scale(FUNDO, (LARGURA_TELA, ALTURA_TELA))

class Fase3:
    def __init__(self, tela):
        self.tela = tela
        self.coelho = Coelho(100, ALTURA_TELA - 150)

        # Moedas (agora com um número reduzido de moedas)
        self.moedas = [
            Moeda(350, ALTURA_TELA - 200),
            Moeda(700, ALTURA_TELA - 100),
        ]

        # Inimigos (com posições e movimentos bem diferentes)
        self.inimigos = [
            Inimigo(150, ALTURA_TELA - 180, "horizontal", 0, 100),  # Inimigo se move horizontalmente
            Inimigo(500, ALTURA_TELA - 175, "vertical", 0, 200),    # Inimigo subindo e descendo
            Inimigo(650, ALTURA_TELA - 150, "horizontal", 100, 300), # Inimigo se move horizontalmente
        ]

        # Obstáculos (agora bem mais difíceis e com diferentes padrões)
        self.obstaculos = [
            Obstaculo(250, ALTURA_TELA - 150),  # Obstáculo difícil de evitar
            Obstaculo(600, ALTURA_TELA - 200),  # Obstáculo difícil de evitar
            Obstaculo(750, ALTURA_TELA - 100),  # Obstáculo difícil de evitar
        ]

        # Bloco de fim de fase
        self.bloco_fim = pygame.Rect(LARGURA_TELA - 50, ALTURA_TELA - 200, 50, 50)

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
            mensagem = font_end.render("Você completou o jogo! Parabéns!", True, (255, 255, 255))
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

        # Verifica colisões com obstáculos
        for obstaculo in self.obstaculos:
            if self.coelho.rect.colliderect(obstaculo.rect):
                self.coelho.perder_vida()

                if self.coelho.vidas <= 0:
                    print("Game Over!")
                    pygame.quit()
                    exit()

        # Verifica o bloco de fim de fase
        if self.coelho.rect.colliderect(self.bloco_fim):
            self.fim_da_fase = True
            self.terminou_fase = True

    def rodar(self):
        self.desenhar()
        self.atualizar()

        if self.fim_da_fase and self.terminou_fase:
            return "fim"  # Finaliza o jogo ou vai para uma tela de congratulações
        return None
