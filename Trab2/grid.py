# Classe base abstrata (Abstract Base Class)
from abc import ABC, abstractmethod
import pygame


# objeto herda de classe abstrata
## nunca pode ser criada, só as filhas
class obj (ABC):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pass


class Grid (obj):

    # só avisa a construtora da mãe o que fazer
    def __init__(self, x, y, size,cell_size):
        super().__init__(x, y)
        self.size = size
        self.cell_size = cell_size
        self.cells = [[Cell(0, 0, row, col) for col in range(size[1])] for row in range(size[0])]
        self.selected_cell:Cell | None = None

        for row in range(size[0]):
            for col in range(size[1]):
                self.cells[row][col].x = self.x + col * cell_size
                self.cells[row][col].y = self.y + row * cell_size

    def draw(self, screen):

        for row in self.cells:
            for cell in row:
                if self.selected_cell is not None:
                    if self.selected_cell.col == cell.col or self.selected_cell.row == cell.row or self.selected_cell.row // 3 == cell.row // 3 and self.selected_cell.col // 3 == cell.col // 3:
                        cell.state = 'highlighted'
                        cell.draw(screen)
                    if self.selected_cell.value == cell.value and self.selected_cell.value is not None:
                        cell.state = 'highlighted'
                        cell.draw(screen)
                    if self.selected_cell == cell:
                        cell.state = 'selected'
                        cell.draw(screen)
                    if not self.is_valid_move(cell,cell.value) and cell.value is not None:
                        cell.valid = False
                        cell.draw(screen)
                cell.state = ''
                cell.draw(screen)  

    def is_valid_move(self, cell,value):
        # Check if the value is already in the same row
        for col in range(self.size[1]):
            other = self.cells[cell.row][col]
            if other != cell and other.value == value:
                return False


        # Check if the value is already in the same column
        for row in range(self.size[0]):
            other = self.cells[row][cell.col]
            if other != cell and other.value == value:
                return False

        # Check if the value is already in the same 3x3 box
        start_row = (cell.row // 3) * 3
        start_col = (cell.col // 3) * 3

        for row in range(start_row, start_row + 3):

            for col in range(start_col, start_col + 3):

                other = self.cells[row][col]

                if other != cell and other.value == value:
                    return False
        return True

    def set_value(self, value):

        if self.selected_cell is None:
            return

        self.selected_cell.value = value

        if self.is_valid_move(self.selected_cell, value):
            self.selected_cell.state = ''
            self.selected_cell.valid = True
        else:
            self.selected_cell.valid = False

    def clear_value(self):

        if self.selected_cell is None:
            return

        self.selected_cell.value = None
        self.selected_cell.state = ''   
        self.selected_cell.valid = True

          


class Cell (obj):

    # só avisa a construtora da mãe o que fazer
    # pode, e deve ser extendido para outras caracteristicas nescessárias
    def __init__(self, x, y, row, col):
        # bom lugar para definir coisas como o fundo da céula
        super().__init__(x, y)
        self.value:int | None = None
        self.row:int = row
        self.col:int = col
        self.valid = True
        self.fixed = False
        self.state:str = ''

    def draw(self,screen):
        if self.state == 'selected':
            pygame.draw.rect(screen, (111, 207, 247), (self.x,self.y, 50, 50), 0)
        elif self.state == 'highlighted':
            pygame.draw.rect(screen, (214, 189, 99), (self.x,self.y, 50, 50), 0)
        elif self.valid == False:
            pygame.draw.rect(screen, (255, 0, 0), (self.x,self.y, 50, 50), 0)

        if self.value is not None:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(str(self.value), True, (30,30,30))
            text_rect = text_surface.get_rect(center=(self.x + 25, self.y + 25))
            screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (150,150,150), (self.x,self.y, 50, 50), 1)

class Button (obj):
    def __init__(self,x,y,size,text):
        super().__init__(x, y)
        self.size = size
        self.text = text

    def draw(self,screen):
        #pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y, self.size[0], self.size[1]))
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.size[0] // 2, self.y + self.size[1] // 2))
        screen.blit(text_surface, text_rect)

    def contains(self, pos):
        x, y = pos

        return (
            self.x <= x < self.x + self.size[0]
            and
            self.y <= y < self.y + self.size[1]
        )

