import pygame
from pygame.locals import *
import random
import os

# Inicialização do Pygame
pygame.init()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Configurações da janela do jogo
largura_tela = 900
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Nyan Cat, The Game")

# Carregar imagem de fundo e redimensioná-la
fundo_imagem = pygame.image.load("IMG/fundo.jpg")
fundo_imagem = pygame.transform.scale(fundo_imagem, (largura_tela, altura_tela))

# Carregar imagens e redimensioná-las
player_imagem = pygame.image.load("IMG/player.png")
player_imagem = pygame.transform.scale(player_imagem, (49, 49))

inimigo_imagem = pygame.image.load("IMG/inimigo.png")
inimigo_imagem = pygame.transform.scale(inimigo_imagem, (30, 30))

tiro_imagem = pygame.image.load("IMG/tiro.png")
tiro_imagem = pygame.transform.scale(tiro_imagem, (10, 20))

# Tamanho e posição inicial do player
tamanho_player = 40
posicao_player_x = largura_tela // 2 - tamanho_player // 2
posicao_player_y = altura_tela - tamanho_player
velocidade_player_x = 5
velocidade_player_y = 0
pulando = False
altura_pulo = 10
contador_pulo = 0

# Tiro
tamanho_tiro = 10
posicao_tiro_x = posicao_player_x + tamanho_player // 2 - tamanho_tiro // 2
posicao_tiro_y = posicao_player_y - tamanho_tiro
velocidade_tiro_y = -10
tiro_ativo = False
tempo_tiro = 0
tempo_espera_tiro = 200  # Tempo em milissegundos

# Inimigos
tamanho_inimigo = 30
posicao_inimigo_x = random.randint(0, largura_tela - tamanho_inimigo)
posicao_inimigo_y = 0
velocidade_inimigo_y = 5
inimigo_ativo = True
numero_inimigos = 5

# Lista de inimigos
inimigos = []
for _ in range(numero_inimigos):
    inimigos.append([random.randint(0, largura_tela - tamanho_inimigo), 0])

# Função para desenhar o player na tela
def desenhar_player():
    tela.blit(player_imagem, (posicao_player_x, posicao_player_y))

# Função para desenhar o tiro na tela
def desenhar_tiro():
    tela.blit(tiro_imagem, (posicao_tiro_x, posicao_tiro_y))

# Função para desenhar os inimigos na tela
def desenhar_inimigos():
    for inimigo in inimigos:
        tela.blit(inimigo_imagem, (inimigo[0], inimigo[1]))

# Verificar colisão entre dois retângulos
def verificar_colisao(retangulo1, retangulo2):
    if retangulo1.colliderect(retangulo2):
        return True
    else:
        return False

# Loop principal do jogo
jogo_ativo = True
clock = pygame.time.Clock()

while jogo_ativo:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            jogo_ativo = False
        
        if event.type == KEYDOWN:
            if event.key == K_a:
                velocidade_player_x = -5
            elif event.key == K_d:
                velocidade_player_x = 5
            elif event.key == K_SPACE and not pulando:
                pulando = True
                velocidade_player_y = -altura_pulo
            elif event.key == K_e and pygame.time.get_ticks() - tempo_tiro >= tempo_espera_tiro:
                tiro_ativo = True
                posicao_tiro_x = posicao_player_x + tamanho_player // 2 - tamanho_tiro // 2
                posicao_tiro_y = posicao_player_y - tamanho_tiro
                tempo_tiro = pygame.time.get_ticks()
    
        if event.type == KEYUP:
            if event.key == K_a or event.key == K_d:
                velocidade_player_x = 0
    
    # Atualizar posição do player
    posicao_player_x += velocidade_player_x
    posicao_player_y += velocidade_player_y
    
    # Atualizar pulo do player
    if pulando:
        contador_pulo += 1
        if contador_pulo > 30:
            pulando = False
            contador_pulo = 0
            velocidade_player_y = altura_pulo
        else:
            velocidade_player_y += 1
    
    # Atualizar posição do tiro
    if tiro_ativo:
        posicao_tiro_y += velocidade_tiro_y
        if posicao_tiro_y < -tamanho_tiro:
            tiro_ativo = False
    
    # Atualizar posição dos inimigos
    for inimigo in inimigos:
        inimigo[1] += velocidade_inimigo_y
        if inimigo[1] > altura_tela:
            inimigo[0] = random.randint(0, largura_tela - tamanho_inimigo)
            inimigo[1] = 0
    
    # Verificar colisão entre player e inimigos
    retangulo_player = pygame.Rect(posicao_player_x, posicao_player_y, tamanho_player, tamanho_player)
    for inimigo in inimigos:
        retangulo_inimigo = pygame.Rect(inimigo[0], inimigo[1], tamanho_inimigo, tamanho_inimigo)
        if verificar_colisao(retangulo_player, retangulo_inimigo):
            jogo_ativo = False
    
    # Verificar colisão entre tiro e inimigos
    retangulo_tiro = pygame.Rect(posicao_tiro_x, posicao_tiro_y, tamanho_tiro, tamanho_player)
    for inimigo in inimigos:
        retangulo_inimigo = pygame.Rect(inimigo[0], inimigo[1], tamanho_inimigo, tamanho_inimigo)
        if verificar_colisao(retangulo_tiro, retangulo_inimigo):
            inimigos.remove(inimigo)
            tiro_ativo = False
    
    # Preencher a tela com a cor branca
    tela.fill((255, 255, 255))
    
    # Desenhar imagem de fundo
    tela.blit(fundo_imagem, (0, 0))
    
    # Desenhar o player na tela
    desenhar_player()
    
    # Desenhar o tiro na tela
    if tiro_ativo:
        desenhar_tiro()
    
    # Desenhar os inimigos na tela
    desenhar_inimigos()
    
    # Atualizar a tela
    pygame.display.update()

# Encerrar o Pygame
pygame.quit()
