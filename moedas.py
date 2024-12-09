import pygame

class Moeda:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/imagens/moeda.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Redimensiona a imagem
        self.rect = self.image.get_rect(topleft=(x, y))
        self.coletada = False

    def verificar_colisao(self, coelho):
        """Verifica se o coelho colidiu com a moeda."""
        return self.rect.colliderect(coelho.rect)

    def desenhar(self, tela):
        """Desenha a moeda na tela apenas se ela não foi coletada."""
        if not self.coletada:
            tela.blit(self.image, self.rect.topleft)
