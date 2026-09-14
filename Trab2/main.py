import pygame
from grid import Grid, Cell

# TRABALHO LUIZ EDUARDO - CAMPO MINADO 90
# TOTAL DE BOMBAS = 10 {PRECISA ACERTAR OS 90 ESPAÇOS RESTANTES}

pygame.init()
pygame.font.init()

# Cria a janela
WIDTH   =  600; HEIGHT =  600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
fpoint = pygame.font.Font(None, 30)  
explosao = pygame.image.load(r"C:\Python\JogosTrab\Trabalho-de-Jogos\Trab2\images\Minado\explosão.png").convert_alpha()
bandeira = pygame.image.load(r"C:\Python\JogosTrab\Trabalho-de-Jogos\Trab2\images\Minado\bandeira.png").convert_alpha()

# Numero de celulas do campo minado
grid_size = (10, 10)
objects = [] #criar objetos, adicione eles a lista
grid = Grid(50, 50, explosao, bandeira, grid_size)
objects.append(grid)
clock = pygame.time.Clock()
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        # Uso do Mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Botão esquerdo
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                grid.clicarmouse(mouse_x, mouse_y)

            # Botão direito
            elif event.button == 3:
                mouse_x, mouse_y = event.pos
                grid.bandeiramouse(mouse_x, mouse_y)

        # Movimento dos teclados através das setas, botão F para colocar e tirar bandeira e
        # SPACE para revelar o espaço e ESC para sair
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()

            elif event.key == pygame.K_UP:
                grid.moverteclado(-1, 0)

            elif event.key == pygame.K_DOWN:
                grid.moverteclado(1, 0)

            elif event.key == pygame.K_LEFT:
                grid.moverteclado(0, -1)

            elif event.key == pygame.K_RIGHT:
                grid.moverteclado(0, 1)

            elif event.key == pygame.K_f:
                grid.bandeirateclado()

            elif event.key == pygame.K_SPACE:
                grid.clicarteclado()

    # Tempo para o looping da animação
    dt = clock.tick(60) /1000
    for obj in objects:
        obj.update(dt)

    # Plano de fundo cinza
    screen.fill((30, 30, 30))

    # Percorrer a lista de objetos
    for obj in objects:
        obj.draw(screen)

    # Texto de pontuação para uma imagem
    textpoints = fpoint.render(f"Pontuação: {grid.pontos}",True,(255, 255, 255))
    screen.blit(textpoints, (50, 15))

    # Texto de Game Over
    if grid.game_over:
        fgame_over = pygame.font.Font(None, 60)
        texto = fgame_over.render("GAME OVER",True,(255, 0, 0))
        px = (WIDTH - texto.get_width()) - 100
        py = 10
        screen.blit(texto, (px, py))

    # Texto de vitória
    if grid.victory:
        font_vitoria = pygame.font.Font(None, 50)
        texto = font_vitoria.render("VOCÊ VENCEU!",True,(0, 200, 0))
        px = WIDTH - texto.get_width() - 100
        py = 10
        screen.blit(texto, (px, py))

    pygame.display.flip()