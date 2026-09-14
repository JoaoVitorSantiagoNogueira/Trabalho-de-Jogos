import pygame
from abc import ABC, abstractmethod
from util import EventHandler

class Player:

    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.vida = 3
        self.angulo = 0
        self.state =  JogadorNormal(self)

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)

    def disparo(self):
        self.state.disparo()

    def disparotriplo(self):
        self.state.disparotriplo()

    def troca_estado(self, new_state):
        self.state.delete()
        self.state = new_state(self)

    # Retirada de vida
    def hit(self):
        self.state.hit()

# Classe base responsável por definir os estados do jogador
class EstadosJogador(ABC):

    def __init__(self, player):
        self.P = player

    # Desenho da nave no centro
    def draw(self, screen):
        sprite = pygame.transform.rotate(self.sprite, self.P.angulo)
        rect = sprite.get_rect(center=self.P.pos)
        screen.blit(sprite, rect)

    def delete(self):
        pass  # se precisar apagar algo na mudança de estados

    @abstractmethod
    def update(self, dt):
        pass

    # Disparo normal
    def disparo(self):
        mouse_pos = pygame.mouse.get_pos()
        EventHandler().notify("Shoot", (self.P.pos, mouse_pos))

    # Disparo triplo, mas curto alcance   
    def disparotriplo(self):
        mouse_pos = pygame.mouse.get_pos()
        EventHandler().notify("TripleShoot", (self.P.pos, mouse_pos))

# Estado padrão do jogador
class JogadorNormal(EstadosJogador):

    # Carregamento da imagem da nave
    def __init__(self, player):
        super().__init__(player)
        self.sprite = pygame.image.load(r"C:\Python\JogosTrab\Trabalho-de-Jogos\Trab3\images\nave.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (70, 70))

    # Movimentação da nave com WASD
    def update(self, dt):
        vel = 5
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.P.pos[1] -= vel
            self.P.angulo = 90
        if keys[pygame.K_s]:
            self.P.pos[1] += vel
            self.P.angulo = -90
        if keys[pygame.K_a]:
            self.P.pos[0] -= vel
            self.P.angulo = 180
        if keys[pygame.K_d]:
            self.P.pos[0] += vel
            self.P.angulo = 0

        # Evita que a nave saia da tela
        self.P.pos.x = max(0, min(768, self.P.pos.x))
        self.P.pos.y = max(0, min(568, self.P.pos.y))

    # Dano tomado
    def hit(self):
        self.P.vida -= 1
        if self.P.vida > 0: # Se tiver vida, ativa o modo invencivel
            self.P.troca_estado(DanoJogador)
        else:
            self.P.troca_estado(JogadorMorto) # Morre

# Momento que o jogador sofre dano e fica invisivel
class DanoJogador(EstadosJogador):

    def __init__(self, player):
        super().__init__(player)
        self.dano = 0 # Tempo do dano até voltar ao normal

        # Imagem da nave
        self.sprite = pygame.image.load(r"C:\Python\JogosTrab\Trabalho-de-Jogos\Trab3\images\nave.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (70, 70))

    def update(self, dt):
        self.dano += dt
        vel = 5
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.P.pos[1] -= vel
            self.P.angulo = 90
        if keys[pygame.K_s]:
            self.P.pos[1] += vel
            self.P.angulo = -90
        if keys[pygame.K_a]:
            self.P.pos[0] -= vel
            self.P.angulo = 180
        if keys[pygame.K_d]:
            self.P.pos[0] += vel
            self.P.angulo = 0

        self.P.pos.x = max(0, min(768, self.P.pos.x))
        self.P.pos.y = max(0, min(568, self.P.pos.y))

        # Tempo de incencibilidade
        if self.dano >= 120:
            self.P.troca_estado(JogadorNormal)

    # Efeito de piscar na tela ao sofrer dano
    def draw(self, screen):
        if (self.dano // 10) % 2 == 0:
            super().draw(screen)

    def disparo(self):
        pass

    def disparotriplo(self):
        pass

    # Invencibilidade
    def hit(self):
        pass

# Quando o jogador morre
class JogadorMorto(EstadosJogador):

    # Nave explode e vira um png de explosão
    def __init__(self, player):
        super().__init__(player)
        self.sprite = pygame.image.load(r"C:\Python\JogosTrab\Trabalho-de-Jogos\Trab3\images\explosão.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))

    def update(self, dt):
        pass

    def disparo(self):
        pass

    def disparotriplo(self):
        pass

    def hit(self):
        pass