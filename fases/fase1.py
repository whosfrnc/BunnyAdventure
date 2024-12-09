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
BLOCO_PRETO = (0, 0, 0)  # Cor do bloco preto

# Redimensiona o fundo para o tamanho da tela
FUNDO = pygame.image.load('assets/imagens/fundoJogo.png')
FUNDO = pygame.transform.scale(FUNDO, (LARGURA_TELA, ALTURA_TELA))

class Fase1:
    def __init__(self, tela):
        self.tela = tela
        self.coelho = Coelho(100, ALTURA_TELA - 150)

        # Moedas (as 4 moedas extras foram removidas)
        self.moedas = [
            Moeda(300, ALTURA_TELA - 200),
            Moeda(500, ALTURA_TELA - 200),
            Moeda(200, ALTURA_TELA - 140),
            Moeda(500, ALTURA_TELA - 140)
        ]

        # Inimigos (os 2 inimigos extras foram removidos)
        self.inimigos = [
            Inimigo(400, ALTURA_TELA - 120, "horizontal", 100, 600),
            Inimigo(600, ALTURA_TELA - 120, "horizontal", 500, 750),
            Inimigo(200, ALTURA_TELA - 150, "horizontal", 100, 300)
        ]

        # Obstáculos (os 3 obstáculos extras foram removidos)
        self.obstaculos = [
            Obstaculo(500, ALTURA_TELA - 200),
            Obstaculo(800, ALTURA_TELA - 100),
            Obstaculo(300, ALTURA_TELA - 140),
            Obstaculo(700, ALTURA_TELA - 140)
        ]

        # Bloco preto para indicar o fim da fase
        self.bloco_fim = pygame.Rect(LARGURA_TELA - 50, ALTURA_TELA - 200, 50, 50)  # Bloco preto que representa o fim da fase

        self.fim_da_fase = False
        self.pontuacao = 0
        self.terminou_fase = False

    def desenhar(self):
        """Desenha o fundo, coelho, moedas, obstáculos, inimigos e o bloco de fim de fase na tela."""
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

        # Se a fase terminou, exibe a mensagem para continuar para a próxima fase
        if self.terminou_fase:
            font_end = pygame.font.Font(None, 48)
            mensagem = font_end.render("Você terminou a fase! Pressione Enter para continuar para a fase 2", True, (255, 255, 255))
            self.tela.blit(mensagem, (LARGURA_TELA / 2 - mensagem.get_width() / 2, ALTURA_TELA / 2))

    def atualizar(self):
        """Atualiza a lógica da fase, como movimentos e verificações de colisões."""
        # Atualiza o coelho
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

        # Verifica o bloco de fim de fase para terminar a fase
        if self.coelho.rect.colliderect(self.bloco_fim):
            self.fim_da_fase = True
            self.terminou_fase = True  # Marca que a fase foi concluída

    def rodar(self):
        """Roda a fase 1 até o fim."""
        self.desenhar()
        self.atualizar()

        if self.fim_da_fase and self.terminou_fase:
            return "fase_2"  # Se a fase for concluída, vai para a fase 2
        return None

    def verificar_game_over(self):
        """Verifica se o jogo terminou devido à perda de todas as vidas."""
        if self.coelho.vidas <= 0:
            print("Game Over!")
            pygame.quit()
            exit()

