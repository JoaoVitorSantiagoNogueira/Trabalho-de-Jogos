import pygame
import math
import random
from player import Player
from bullet import BaladoJogador
from util import EventHandler, circle_collistiion

# Representa o inimigo, guardando as informações essenciais
class Enemy:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.raio = 16
        self.vidainimigo = 3 # Vida do inimigo
        self.estado = EnemyMovimento(self)

    def destroy(self):
        EventHandler().notify("DestroyObj", self)

    # Mudança de estado para lentidão
    def troca_estado(self, new_estado):
        self.estado = new_estado(self)

    def update(self, dt):
        self.estado.update(dt)

    def draw(self, screen):
        self.estado.draw(screen)

# Inimigo se aproximando do jogador, definindo o comportamento do adversário
class EnemyMovimento:
    def __init__(self, enemy):
        self.enemy = enemy # refência do inimigo
        self.vel = 1.3 # velocidade do inimigo
        self.sprite = pygame.Surface((self.enemy.raio * 2, self.enemy.raio * 2))
        self.sprite.set_colorkey((0, 0, 0))

        # Desenho do inimigo
        pygame.draw.circle(self.sprite,(255,215,0),
                           (self.enemy.raio, self.enemy.raio),self.enemy.raio)

    # Calcula onde está o jogador e vai em direção a ele
    def update(self, dt):

        # Enquanto o jogador estiver vivo
        if player.vida > 0:
            direction = pygame.Vector2( player.pos[0] - self.enemy.pos[0],player.pos[1]
                        - self.enemy.pos[1])

            # Evitar que ele passe do jogador
            if direction.length() > 0:
                direction = direction.normalize()

            self.enemy.pos += direction * self.vel

    def draw(self, screen):
        screen.blit(self.sprite, self.enemy.pos)

   
# Inimigo recebe dano e fica lento
class EnemyLento:
    def __init__(self, enemy):
        self.enemy = enemy
        self.Tempdeco = 0 # tempo decorrido
        self.vel = 0.5
        self.sprite = pygame.Surface((self.enemy.raio * 2, self.enemy.raio * 2))
        self.sprite.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.sprite,(176,196,222),
            (self.enemy.raio, self.enemy.raio),self.enemy.raio)

    # mesma ideia do inimigo se movimentando, mas com o tempo de lentidão ao sofrer dano
    def update(self, dt):
        if player.vida > 0:
            self.Tempdeco += dt
            direction = pygame.Vector2(player.pos[0] - self.enemy.pos[0],
                                    player.pos[1] - self.enemy.pos[1])

            if direction.length() > 0:
                direction = direction.normalize()

            self.enemy.pos += direction * self.vel
            if self.Tempdeco >= 120:
                self.enemy.troca_estado(EnemyMovimento)

    def draw(self, screen):
        screen.blit(self.sprite, self.enemy.pos)






#inicialização
pygame.init()
WIDTH   =  800; HEIGHT =  600
clock = pygame.time.Clock()
font = pygame.font.SysFont("Times New Roman", 36)
fontfim = pygame.font.SysFont("Arial", 70)
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
background = pygame.image.load(r"C:\Python\JogosTrab\Trabalho-de-Jogos\Trab3\images\espaço.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player = Player((400, 300)) # Nave no meio
objects = []
objects.append(player)
pontos = 0
enemy = Enemy((100, 100))
objects.append(enemy)

# funções de controle do player 
def handle_input(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN: # Ação do mouse
            if event.button == 1:
                player.disparo() # tiro comum (botão esquerdo)
            elif event.button == 3:
                player.disparotriplo() # Tiro triplo, mas curto alcance (botão direito)

def remove_obj(obj):
    #variavel global é feio, mas serve como um exemplo
    if obj in objects:
        objects.remove(obj) 

# criar disparo normal
def criarbala(data):
    player_pos, mouse_pos = data
    dx = mouse_pos[0] - player_pos[0]
    dy = mouse_pos[1] - player_pos[1]
    angulo = math.degrees(math.atan2(dy, dx))
    bala = BaladoJogador(player_pos, angulo, life_time=240)
    objects.append(bala)

# criar triplo disparo
def dis3create(data):
    player_pos, mouse_pos = data
    dx = mouse_pos[0] - player_pos[0]
    dy = mouse_pos[1] - player_pos[1]
    angulo = math.degrees(math.atan2(dy, dx))
    for angulo in (angulo-15, angulo, angulo+15):
        bala = BaladoJogador(player_pos, angulo, life_time=15)
        objects.append(bala)


# Criando vários inimigos
def criarenemy():
    side = random.randint(0, 3)
    if side == 0:
        pos = (random.randint(0, WIDTH), 0)

    elif side == 1:
        pos = (random.randint(0, WIDTH), HEIGHT)

    elif side == 2:
        pos = (0, random.randint(0, HEIGHT))

    else:
        pos = (WIDTH, random.randint(0, HEIGHT))

    enemy = Enemy(pos)
    objects.append(enemy)

# Dano ao inimigo
def hitenemy(data):
    global pontos # Pontuação ao vencer o inimigo
    enemy, bala = data
    enemy.vidainimigo -= 1
    bala.destroy() # bala destroi ao atingir o inimigo
    
    # Diminui o tamanho a cada dano, se chegar a zero, some
    if enemy.vidainimigo > 0:
        enemy.raio = 6+(enemy.vidainimigo*4)
        enemy.troca_estado(EnemyLento)
    else:
        enemy.destroy()
        pontos += 1

# Verificação de colisões
def verificarcolisão():

    # Vetores para armazenar os objetos das balas e inimigos
    vetbalas = []
    enemies = []
    for obj in objects:
        if isinstance(obj, BaladoJogador):
            vetbalas.append(obj)

        if isinstance(obj, Enemy):
            enemies.append(obj)

    # Para cada bala, verifica todos os inimigos
    for bala in vetbalas:
        for enemy in enemies:

            # Circulo que define a colisão (HitBox), 
            # Verifica se a distância entre esses dois círculos é menor ou igual à soma dos seus raios
            # Se for, colidiu
            if circle_collistiion(bala.pos,bala.radius,enemy.pos,enemy.raio):
                EventHandler().notify("HitEnemy", (enemy, bala)) # informa que acertou o inimigo
                break

    # Se o inimigo colidir com o jogador, da um dano no jogador e o inimigo explode
    for enemy in enemies:
        if circle_collistiion(enemy.pos,enemy.raio,player.pos,16):
            player.hit()
            enemy.destroy()

# Determinação dos eventos e a execução deles
EventHandler().subscribe("DestroyObj", remove_obj)
EventHandler().subscribe("Shoot", criarbala)
EventHandler().subscribe("TripleShoot", dis3create)
EventHandler().subscribe("HitEnemy", hitenemy)






# loop principal
tempenemy = 0
running = True
while running:

    # A cada 10pts feitos, mais inimigos aparecem
    if player.vida > 0:
        tempenemy += 1
        if tempenemy >= 200:
            quantidade = pontos // 10 + 1 # A cada 10pts, o spawm dos inimigos aumenta em 1
            for i in range(quantidade):
                criarenemy()
            tempenemy = 0

    handle_input(player)
    for obj in objects:
        obj.update(1)

    verificarcolisão()
    screen.blit(background, (0, 0))

    for obj in objects:
        obj.draw(screen)

    # Demonstração da pontuação e vidas
    pontostext = font.render("Pontos: " + str(pontos), True, (135,206,250))
    screen.blit(pontostext, (10, 10))
    health_text = font.render("Vida: " + str(player.vida), True, (144,238,144))
    screen.blit(health_text, (10, 45))

    # Mensagem de Game Over se o jogador morrer, colocando ela no meio
    if player.vida <= 0:
        gameovertext = fontfim.render("GAME OVER", True, (139,0,0))
        gameover = gameovertext.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(gameovertext, gameover)

    pygame.display.flip()
    clock.tick(60)