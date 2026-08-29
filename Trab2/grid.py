import pygame
import random
from abc import ABC, abstractmethod

class obj (ABC):
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.sprites = sprites

    def draw(self, screen):
        for s in self.sprites:
            screen.blit(self.sprites, (self.x, self.y))

    @abstractmethod
    def update(self, dt):
        pass

class Grid (obj):
    def __init__(self, x, y, explosao, bandeira, grid_size):
        super().__init__(x, y, [])

        self.cells = [] # Armazenar as células
        self.game_over = False # Mensagem de fim de jogo
        self.victory = False # Vitoria
        self.sel_linha = 0 # posição inicial do teclado
        self.sel_coluna = 0
        self.pontos = 0 # Contador de pontos

        lin, col = grid_size # Separação de linhas e colunas da grade do campo minado
        for l in range(lin):
            linatual = [] # Linha atual

            for c in range(col):
                cell = Cell(x + c * 50,y + l * 50, 50, explosao, bandeira) # Psoição da célula
                linatual.append(cell)

            self.cells.append(linatual)

        self.putbombas(10) # Numero de bombas
        self.calculoentorno()

    # Atualização dos pontos
    def atualizar_pontos(self):
        self.pontos = 0
        for linha in self.cells:
            for cell in linha:
                if cell.revelada:
                    self.pontos += 1

    # Função de verificar se o jogador acertou todos os quadrados
    def checkvitoria(self):
        for linha in self.cells:
            for cell in linha:

                # Se existe uma célula sem bomba
                # que ainda não foi revelada,
                # o jogador ainda não ganhou.
                if not cell.bomba and not cell.revelada:
                    return False

        return True

    # Função para instalação das bombas aleatoriamentes pelo grid
    def putbombas(self, quantidade):
        posicoes = []
        for l in range(len(self.cells)):
            for c in range(len(self.cells[0])):
                posicoes.append((l, c))

        minas = random.sample(posicoes, quantidade)
        for l, c in minas:
            self.cells[l][c].bomba = True

    # Função para calcular se exite minas em volta
    def calculoentorno(self):
        linhas = len(self.cells)
        colunas = len(self.cells[0])
        for l in range(linhas):
            for c in range(colunas):
                if self.cells[l][c].bomba:
                    continue

                cont = 0
                for dl in range(-1, 2):
                    for dc in range(-1, 2):
                        if dl == 0 and dc == 0:
                            continue

                        vizlinha = l + dl
                        vizcoluna = c + dc
                        if 0 <= vizlinha < linhas and 0 <= vizcoluna < colunas:
                            if self.cells[vizlinha][vizcoluna].bomba:
                                cont += 1

                self.cells[l][c].cont = cont

    # Movimento de teclado
    def moverteclado(self, dl, dc):
        if self.game_over or self.victory:
            return

        novalinha = self.sel_linha + dl
        novacoluna = self.sel_coluna + dc
        if 0 <= novalinha < len(self.cells) and 0 <= novacoluna < len(self.cells[0]):
            self.sel_linha = novalinha
            self.sel_coluna = novacoluna

    # Revelação dos espaços em cadeia
    def revelarcadeia(self, lin, col):
        linhas = len(self.cells)
        colunas = len(self.cells[0])

        # Lista de células que ainda precisam ser verificadas, 
        # guardando sempre as células de 0 
        fila = [(lin, col)]

        while fila:
            atuallinha, atualcoluna = fila.pop(0)
            cell = self.cells[atuallinha][atualcoluna]

            # Se já foi revelada, não faz nada
            if cell.revelada:
                continue

            # Nunca revela uma bomba pela cadeia
            if cell.bomba:
                continue

            # Revela a célula
            cell.revelar()

            # Se tiver número, não continua a partir dela
            if cell.cont > 0:
                continue

            # Se for zero, verifica os 8 vizinhos
            for dl in range(-1, 2):
                for dc in range(-1, 2):

                    if dl == 0 and dc == 0:
                        continue

                    vizlinha = atuallinha + dl
                    vizcoluna = atualcoluna + dc

                    # Verifica se está dentro da grade
                    if 0 <=  vizlinha < linhas and 0 <= vizcoluna < colunas:
                        vizinha = self.cells[ vizlinha][vizcoluna]

                        # Só adiciona células que não são bombas
                        # e ainda não foram reveladas
                        if not vizinha.bomba and not vizinha.revelada and not vizinha.band:
                            fila.append(( vizlinha, vizcoluna))

    # Comando da bandeira com o mouse
    def bandeiramouse(self, mouse_x, mouse_y):
        if self.game_over or self.victory:
            return

        # Localização do cursor para o clique na coluna e linha correta
        col = (mouse_x - self.x) // 50
        lin = (mouse_y - self.y) // 50
        if 0 <= lin < len(self.cells) and 0 <= col < len(self.cells[0]):
            cell = self.cells[lin][col]
            cell.putbandeira()

    # Comando da bandeira com o teclado
    def bandeirateclado(self):
        if self.game_over or self.victory:
            return

        cell = self.cells[self.sel_linha][self.sel_coluna]
        cell.putbandeira()

    # Função de clicar no mouse, descobrindo a célula clicada
    def clicarmouse(self, mouse_x, mouse_y): 
            if self.game_over or self.victory: # Se acabou o jogo, encerra
                return
    
            col = (mouse_x - self.x) // 50 # Reajuste no grid para encontrar a célula
            lin = (mouse_y - self.y) // 50
            if 0 <= lin < len(self.cells) and 0 <= col < len(self.cells[0]): # Analise da grade, ver se ele está lá dentro
                cell = self.cells[lin][col]

                # Se clicou em uma bomba
                if cell.bomba:
                    self.game_over = True
                    cell.explodir()
    
                    # Revela todas as outras bombas
                    for linha in self.cells:
                        for cellnext in linha:
                            if cellnext.bomba:
                                cellnext.revelada = True
    
                else:
                    # Se não for bomba, revela normalmente, onde tambem revelará as outras em cadeia
                    # até bater em um numero
                    if cell.cont == 0:
                        self.revelarcadeia(lin, col)
                    else:
                        cell.revelar()
    
                    self.atualizar_pontos()
                    if self.checkvitoria():
                        self.victory = True

    # Função de clicar no teclado 
    def clicarteclado(self):
        x = self.x + self.sel_coluna * 50 + 25
        y = self.y + self.sel_linha * 50 + 25
        self.clicarmouse(x, y)

    # Desenha o conjunto de células
    def draw(self, screen):
        for l in range(len(self.cells)):
            for c in range(len(self.cells[0])):
                cell = self.cells[l][c]

                # Define qual célula está selecionada
                cell.selecionada = (l == self.sel_linha and c == self.sel_coluna)
                cell.draw(screen)

    # Atualiza o conjunto de células
    def update(self, dt):
        if self.game_over or self.victory:
                return
         
        for linha in self.cells:
            for cell in linha:
                cell.update(dt)

class Cell (obj):

    def __init__(self, x, y, tam, explosao, bandeira):
        super().__init__(x, y, [])
        self.tam = tam # Tamanho da célula
        self.bomba = False # Possui uma bomba?
        self.band = False # Possui uma bandeira?
        self.bandeira = bandeira # Imagem da bandeira
        self.revelada = False # Célula foi aberta?
        self.explodindo = False # Bomba explodiu?
        self.explosao = explosao # Imagem da explosão
        self.cont = 0 # Contador de bombas ao redor da célula
        self.selecionada = False # Célula selecionada pelo teclado
        self.tempanimacao = 0 # Contador de tempo para animação do teclado
        self.corcursor = (255, 255, 0) # Cor do teclado
        self.font = pygame.font.Font(None, 36) # Fonte do contador das bombas ao redor

    def revelar(self): # Revelar célula
        self.revelada = True

    def explodir(self): # Clicou na bomba
        self.explodindo = True

    def putbandeira(self): # Colocar a bandeira
        if not self.revelada:
            self.band = not self.band

    # Desenho da célula
    def draw(self, screen):
        if self.revelada: # Célula foi revelada? Se sim, quadrado cinza
            pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y, self.tam, self.tam))
        else: # Se não, mantem fechada
            pygame.draw.rect(screen, (80, 80, 80), (self.x, self.y, 50, 50))
            pygame.draw.rect(screen, (30, 30, 30), (self.x, self.y, 50, 50),1)

        if self.revelada and self.cont > 0: # Desenho do numero das bombas proximas
            text = self.font.render(str(self.cont), True, (0, 0, 0))
            px = self.x + (self.tam-text.get_width()) // 2
            py = self.y + (self.tam-text.get_height()) // 2
            screen.blit(text, (px, py))

        if self.band and not self.revelada: # Desenho da bandeira
            imgbandeira = pygame.transform.scale(self.bandeira,(self.tam, self.tam))
            screen.blit(imgbandeira, (self.x, self.y))

        if self.revelada and self.bomba: # Mostra as bombas depois do Game Over
            cx = self.x + self.tam // 2
            cy = self.y + self.tam // 2
            pygame.draw.circle(screen,(20, 20, 20),(cx, cy),15)

        if self.explodindo: # Mostra a explosão da bomba clicada
            explosao = pygame.transform.scale(self.explosao,(self.tam, self.tam))
            screen.blit(explosao,(self.x, self.y))

        if self.selecionada: # Cor da borda do teclado
            pygame.draw.rect(screen,self.corcursor,(self.x, self.y, self.tam, self.tam),3)

    # Atualização nas cores do cursor do teclado entre amarelo e laranja, da célula
    def update(self, dt):
        if self.selecionada:
            self.tempanimacao += dt
            if self.tempanimacao >= 0.5:
                self.tempanimacao = 0
                if self.corcursor == (255, 255, 0):
                    self.corcursor = (165, 165, 10)
                else:
                    self.corcursor = (255, 255, 0)
        else:
            self.tempanimacao = 0
            self.corcursor = (255, 255, 0)
