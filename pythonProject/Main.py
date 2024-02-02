import pygame
from sprites import *
from config import *
from Character.MapLoader import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.WIN_WIDTH, Config.WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.character_spritesheet = Spritesheet("assets/character.png")
        self.terrain_spritesheet = Spritesheet("assets/terrain.png")
        self.water_spritesheet = Spritesheet("assets/water_tileset.png")

    def createTileMap(self):
        ml = MapLoader()
        self.bombas = ml.bombas
        self.diamantes = ml.diamantes
        self.pociones = ml.pociones
        self.snorkel = ml.trajes
        for _ in range(self.bombas):
            generado = False
            while not generado:
                y, x = random.randint(0, 39), random.randint(0, 20)
                if Config.maptile[x][y] == '.':
                    generado = True
                    fila = Config.maptile[x]
                    nueva_fila = fila[:y] + 'B' + fila[y + 1:]
                    Config.maptile[x] = nueva_fila
        for _ in range(self.pociones):
            generado = False
            while not generado:
                y, x = random.randint(0, 39), random.randint(0, 20)
                if Config.maptile[x][y] == '.':
                    generado = True
                    fila = Config.maptile[x]
                    nueva_fila = fila[:y] + 'C' + fila[y + 1:]
                    Config.maptile[x] = nueva_fila
        for _ in range(self.diamantes):
            generado = False
            while not generado:
                y, x = random.randint(0, 39), random.randint(0, 20)
                if Config.maptile[x][y] == '.':
                    generado = True
                    fila = Config.maptile[x]
                    nueva_fila = fila[:y] + 'D' + fila[y + 1:]
                    Config.maptile[x] = nueva_fila
        for _ in range(self.snorkel):
            generado = False
            while not generado:
                y, x = random.randint(0, 39), random.randint(0, 20)
                if Config.maptile[x][y] == '.':
                    generado = True
                    fila = Config.maptile[x]
                    nueva_fila = fila[:y] + 'T' + fila[y + 1:]
                    Config.maptile[x] = nueva_fila


        for i, row in enumerate(Config.maptile):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "M":
                    Block(self, j, i)
                if column == "P":
                    Player(self, j, i)
                if column == "A":
                    Water(self, j, i)
                if column == "C":
                    Pocion(self, j, i)
                if column == "B":
                    Bomba(self, j, i)
                if column == "D":
                    Diamante(self, j, i)
                if column == "T":
                    Snorkel(self, j, i)




    def new(self):

        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()

        self.createTileMap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(Config.BLACK)

        self.all_sprites.draw(self.screen)
        self.clock.tick(Config.FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass


g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
