import pygame

class Inimigo:
    def __init__(self, x, y, direcao, limite_esq, limite_dir):
        self.image = pygame.image.load('assets/imagens/inimigo.png')
        self.image = pygame.transform.scale(self.image, (40, 40))  # Redimensiona a imagem
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = 2
        self.direcao = direcao
        self.limite_esq = limite_esq
        self.limite_dir = limite_dir

    def mover(self):
        if self.direcao == "horizontal":
            self.rect.x += self.velocidade
            if self.rect.x >= self.limite_dir or self.rect.x <= self.limite_esq:
                self.velocidade *= -1

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)
