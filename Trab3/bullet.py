import pygame
from abc import ABC, abstractmethod
from util import EventHandler
import math

# Rotação da bala
def rotate(pos, angle, axis = (0,0)):
    angle = math.radians(angle) # conversão dos angulos

    # separa as coordenadas da posição
    x, y = pos
    ax, ay = axis

    # move o ponto para considerar o eixo de rotação como origem
    x -= ax
    y -= ay

    # calcula seno e cosseno do ângulo
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    # aplica a fórmula matemática de rotação
    rx = x * cos_a - y * sin_a
    ry = x * sin_a + y * cos_a

    # retorna a posição após a rotação
    return rx + ax, ry + ay

# Modelo da bala
class Bala (ABC):
    def __init__(self, pos, angle = 0, radius = 16, life_time = None):
        self.pos = pos
        self.origin = pygame.Vector2(pos)
        self.life_time = life_time
        self.angulo = angle # Angulo da bala
        self.elapsed = 0 # Tempo da bala vive
        self.radius = radius # Raio da bala

    # Atualização da bala a cada frame
    def update(self, dt):
        self.elapsed += dt
        if self.life_time and self.elapsed >= self.life_time: # Tempo de vida da bala
                self.destroy() # destroi ela

        # Recolocação da bala
        self.pos = rotate(self.move(), self.angulo)+self.origin

    # Desenha a bala
    def draw(self, screen):
        screen.blit(self.sprite, self.pos)

    @abstractmethod
    def move(self):
        pass

    def destroy(self): # pede para deletar
        EventHandler().notify("DestroyObj", self) # avisa o mundo que saiu da tela


# A bala da nave, em formato retangular
class BaladoJogador(Bala):
    def __init__(self, pos, angle=0, life_time=None):
        super().__init__(pos, angle, radius=5, life_time=life_time)
        self.sprite = pygame.Surface((20, 8))
        self.sprite.fill((0,255,255))
        self.sprite = pygame.transform.rotate(self.sprite, -angle)

    def move(self):
        vel = 12 # Velocidade do disparo
        return pygame.Vector2(self.elapsed * vel, 0)

    def update(self, dt):
        super().update(dt)
        if (self.pos[0] < 0 or self.pos[0] > 800 or
            self.pos[1] < 0 or self.pos[1] > 600):
            self.destroy()