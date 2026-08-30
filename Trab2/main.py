import pygame
from grid import Grid, Cell, Button


pygame.init()
pygame.font.init()

WIDTH   =  1280; HEIGHT =  720
screen = pygame.display.set_mode((WIDTH, HEIGHT))  

# caso precise de usar fontes na main, descomente
font_size = 25
font = pygame.font.Font(None, font_size)

#numero de celulas
grid_size = (9, 9)
cell_size = 50
grid = Grid((WIDTH - grid_size[0]*cell_size) // 2,0, grid_size, cell_size)

BUTTON_SIZE = 45
BUTTON_GAP = 5
NUM_BUTTONS = 10

# Largura total dos 9 botões + espaços
total_width = NUM_BUTTONS * BUTTON_SIZE + (NUM_BUTTONS-1) * BUTTON_GAP

# Centro horizontal do grid
grid_center = grid.x + (grid_size[0] * cell_size) // 2

# Posição X inicial dos botões
start_x = grid_center - total_width // 2

# Parte inferior do grid
grid_bottom = grid.y + grid_size[1] * cell_size

# Altura disponível abaixo do grid
remaining_height = HEIGHT - grid_bottom

# Posição Y para centralizar verticalmente os botões
buttons_y = grid_bottom + (remaining_height - BUTTON_SIZE) // 2

buttons = [
    Button(
        start_x + i * (BUTTON_SIZE + BUTTON_GAP),
        buttons_y,
        (BUTTON_SIZE, BUTTON_SIZE),
        str(i + 1)
    )
    for i in range(9)
]

buttons.append(
    Button(
        start_x + 9 * (BUTTON_SIZE + BUTTON_GAP),
        buttons_y,
        (BUTTON_SIZE, BUTTON_SIZE),
        "X"
    )
) 

while True: 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        # uso do mouse é obrigatório
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] > grid.x and event.pos[0] < grid.x + grid.size[0]*grid.cell_size and event.pos[1] > grid.y and event.pos[1] < grid.y + grid.size[1]*grid.cell_size:
                col = (event.pos[0] - grid.x) // grid.cell_size
                row = (event.pos[1] - grid.y) // grid.cell_size
                print(f"selected cell: ({row},{col})")
                grid.selected_cell = grid.cells[row][col]

            else:
                for button in buttons:

                    if button.contains(event.pos):
                        print(f"button {button.text} pressed")

                        if grid.selected_cell is not None:
                            if grid.selected_cell.fixed == False: 
                                if button.text == "X":
                                    grid.clear_value()
                                else:
                                    value = int(button.text)
                                    grid.set_value(value)




        # uso do teclado para controle é obrigatório
        elif event.type == pygame.KEYDOWN:
            #inclua outras funcionalidades para outras téclas
            if event.key == pygame.K_ESCAPE:
                exit()
            if grid.selected_cell is None:
                if event.key == pygame.K_UP:
                    grid.selected_cell = grid.cells[0][0] 
                if event.key == pygame.K_DOWN:
                    grid.selected_cell = grid.cells[0][0] 
                if event.key == pygame.K_LEFT:
                    grid.selected_cell = grid.cells[0][0] 
                if event.key == pygame.K_RIGHT:
                    grid.selected_cell = grid.cells[0][0] 
            if grid.selected_cell:
                if event.key == pygame.K_UP:
                    grid.selected_cell = grid.selected_cell.row - 1 >= 0 and grid.cells[grid.selected_cell.row - 1][grid.selected_cell.col] or grid.selected_cell
                if event.key == pygame.K_DOWN:
                    grid.selected_cell = grid.selected_cell.row + 1 < grid_size[0] and grid.cells[grid.selected_cell.row + 1][grid.selected_cell.col] or grid.selected_cell
                if event.key == pygame.K_LEFT:
                    grid.selected_cell = grid.selected_cell.col - 1 >= 0 and grid.cells[grid.selected_cell.row][grid.selected_cell.col - 1] or grid.selected_cell
                if event.key == pygame.K_RIGHT:
                    grid.selected_cell = grid.selected_cell.col + 1 < grid_size[1] and grid.cells[grid.selected_cell.row][grid.selected_cell.col + 1] or grid.selected_cell
                if pygame.K_1 <= event.key <= pygame.K_9 and grid.selected_cell.fixed == False:
                    value = event.key - pygame.K_0
                    grid.set_value(value)
                if event.key == pygame.K_BACKSPACE and grid.selected_cell.fixed == False:
                    grid.clear_value()

        # Desenha
        screen.fill((255,255,255))
        grid.draw(screen)  # Draw the grid with white color
        for button in buttons:
            button.draw(screen)

        if grid.is_full():
            font = pygame.font.Font(None, 36)
            text_surface = font.render("Congratulations! You solved the puzzle!", True, (0, 255, 0))
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_surface, text_rect)
        

        pygame.display.flip()