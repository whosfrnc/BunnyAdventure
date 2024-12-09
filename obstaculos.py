import pygame

class Obstaculo:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/imagens/obstaculo.png')
        self.image = pygame.transform.scale(self.image, (40, 40))  # Redimensiona a imagem
        self.rect = self.image.get_rect(topleft=(x, y))

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)
