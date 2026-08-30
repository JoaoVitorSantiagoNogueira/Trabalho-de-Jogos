# Classe base abstrata (Abstract Base Class)
from abc import ABC, abstractmethod
import pygame
import random


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

        self.new_game()

    def draw(self, screen):

        for row in self.cells:
            for cell in row:

                cell.state = ''

                if self.selected_cell is not None:

                    if cell.valid == False:
                        cell.state = 'invalid'

                    elif self.selected_cell == cell:
                        cell.state = 'selected'

                    elif (
                        self.selected_cell.col == cell.col
                        or self.selected_cell.row == cell.row
                        or (
                            self.selected_cell.row // 3 == cell.row // 3
                            and self.selected_cell.col // 3 == cell.col // 3
                        )
                    ):
                        cell.state = 'highlighted'

                    elif (
                        self.selected_cell.value is not None
                        and self.selected_cell.value == cell.value
                    ):
                        cell.state = 'highlighted'

                cell.draw(screen)

        line_width = 3
        grid_size = self.size[0] * self.cell_size

        for i in range(0, 10, 3):

            # linha horizontal
            y = self.y + i * self.cell_size

            pygame.draw.line(
                screen,
                (0, 0, 0),
                (self.x, y),
                (self.x + grid_size, y),
                line_width
            )

            # linha vertical
            x = self.x + i * self.cell_size

            pygame.draw.line(
                screen,
                (0, 0, 0),
                (x, self.y),
                (x, self.y + grid_size),
                line_width
            )

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

        cell = self.selected_cell

        cell.value = value
        cell.valid = self.is_valid_move(cell, value)

    def clear_value(self):

        if self.selected_cell is None:
            return

        self.selected_cell.value = None
        self.selected_cell.state = ''   
        self.selected_cell.valid = True

    def new_game(self,difficulty = 0.3):
        self.fill_grid()

        for row in self.cells:
            for cell in row:
                if random.random() > difficulty:
                    cell.value = None
                    cell.fixed = False
                else:
                    cell.fixed = True

    def find_empty_cell(self):
        for row in self.cells:
            for cell in row:
                if cell.value is None:
                    return cell
        return None

    def fill_grid(self):

        empty = self.find_empty_cell()

        if empty is None:
            return True

        numbers = list(range(1, 10))
        random.shuffle(numbers)

        for number in numbers:

            if self.is_valid_move(empty, number):
                row, col = empty.row, empty.col
                self.cells[row][col].value = number

                if self.fill_grid():
                    return True

                self.cells[row][col].value = None

        return False

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value is None:
                    return False
        return True


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
        elif self.state == 'invalid':
            pygame.draw.rect(screen, (255, 0, 0), (self.x,self.y, 50, 50), 0)

        if self.value is not None:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(str(self.value), True, (80,80,80))
            if self.fixed:
                text_surface = font.render(str(self.value), True, (0,0,0))
            text_rect = text_surface.get_rect(center=(self.x + 25, self.y + 25))
            screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (150,150,150), (self.x,self.y, 50, 50), 1)

class Button (obj):
    def __init__(self,x,y,size,text):
        super().__init__(x, y)
        self.size = size
        self.text = text
        self.text_surface = pygame.font.Font(None, 36).render(text, True, (0, 0, 0))

    def draw(self, screen):

        text_rect = self.text_surface.get_rect(
            center=(
                self.x + self.size[0] // 2,
                self.y + self.size[1] // 2
            )
        )

        screen.blit(self.text_surface, text_rect)

    def contains(self, pos):
        x, y = pos

        return (
            self.x <= x < self.x + self.size[0]
            and
            self.y <= y < self.y + self.size[1]
        )

