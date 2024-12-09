import pygame
from config import ALTURA_TELA, LARGURA_TELA
import time

class Coelho:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/imagens/coelho.gif").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensiona a imagem
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = 5
        self.velocidade_pulo = 0
        self.gravidade = 1
        self.no_chao = False
        self.moedas = 0
        self.vidas = 3
        self.tempo_invulnerabilidade = 0  # Tempo de invulnerabilidade (em segundos)
        self.invulneravel = False  # Flag que indica se o coelho está invulnerável

    def pular(self):
        """Faz o coelho pular se ele estiver no chão."""
        if self.no_chao:
            self.velocidade_pulo = -15
            self.no_chao = False

    def atualizar(self):
        """Atualiza a posição do coelho com base no teclado e na gravidade."""
        keys = pygame.key.get_pressed()

        # Movimento horizontal
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT] and self.rect.right < LARGURA_TELA:
            self.rect.x += self.velocidade

        # Pulo
        if keys[pygame.K_SPACE]:
            self.pular()

        # Aplicação da gravidade
        self.rect.y += self.velocidade_pulo
        self.velocidade_pulo += self.gravidade

        # Verificação de contato com o chão
        if self.rect.y >= ALTURA_TELA - 100:  # Chão da tela
            self.rect.y = ALTURA_TELA - 100
            self.no_chao = True
            self.velocidade_pulo = 0

        # Atualiza o tempo de invulnerabilidade
        if self.invulneravel and time.time() - self.tempo_invulnerabilidade >= 1.5:
            self.invulneravel = False

    def coletar_moeda(self, moeda):
        """Incrementa o número de moedas se o coelho colidir com uma moeda não coletada."""
        if moeda.verificar_colisao(self) and not moeda.coletada:
            moeda.coletada = True
            self.moedas += 1
            if self.moedas % 5 == 0:  # Ganha uma vida a cada 5 moedas
                self.vidas += 1

    def perder_vida(self):
        """Reduz uma vida do coelho."""
        if not self.invulneravel:  # Só perde vida se não estiver invulnerável
            self.vidas -= 1
            self.invulneravel = True  # Ativa a invulnerabilidade
            self.tempo_invulnerabilidade = time.time()  # Marca o início da invulnerabilidade

    def desenhar(self, tela):
        """Desenha o coelho na tela."""
        tela.blit(self.image, self.rect.topleft)
