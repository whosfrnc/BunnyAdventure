import pygame
from config import *
from fases.fase1 import Fase1
from fases.fase2 import Fase2
from fases.fase3 import Fase3  # Nova fase"

# Inicializando o Pygame
pygame.init()
pygame.mixer.init()

# Configuração da tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Aventura do Coelho")

# Controle de FPS
clock = pygame.time.Clock()

def tela_inicial(tela):
    """Exibe a tela de introdução."""
    fonte = pygame.font.Font(None, 48)
    texto_inicio = fonte.render("Pressione ENTER para Iniciar <br> Os inimigos causam dano e os obstaculos também, cuidado", True, (255, 255, 255))
    tela.fill((0, 0, 0))
    tela.blit(texto_inicio, (tela.get_width() // 2 - texto_inicio.get_width() // 2, tela.get_height() // 2))
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return

def tela_fim_fase(tela):
    """Exibe a tela de transição."""
    fonte = pygame.font.Font(None, 48)
    texto = fonte.render("Fase concluída! Pressione ENTER para continuar.", True, (255, 255, 255))
    tela.fill((0, 0, 0))
    tela.blit(texto, (tela.get_width() // 2 - texto.get_width() // 2, tela.get_height() // 2))
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return

def main():
    tela_inicial(tela)

    fases = [Fase1(tela), Fase2(tela), Fase3(tela)]  # Lista de fases
    for fase in fases:
        fase_concluida = False
        while not fase_concluida:
            clock.tick(FPS)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            fase_concluida = fase.rodar()  # Executa a fase e verifica se foi concluída
            pygame.display.flip()
        tela_fim_fase(tela)  # Exibe a transição após a fase

    print("Parabéns! Você concluiu todas as fases.")
    pygame.quit()

if __name__ == "__main__":
    main()
