import pygame

import sprites
from sprites import *
from config import *
from Character.MapLoader import *
import sys


class Game:
    objetivo = 0
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((Config.WIN_WIDTH, Config.WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.character_spritesheet = Spritesheet("assets/character.png")
        self.terrain_spritesheet = Spritesheet("assets/terrain.png")
        self.water_spritesheet = Spritesheet("assets/water_tileset.png")

    def createTileMap(self):
        ml = MapLoader()
        self.bombas = ml.bombas
        self.diamantes, self.objetivo = ml.diamantes, ml.diamantes
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
        self.water = pygame.sprite.LayeredUpdates()
        self.item_snorkel = pygame.sprite.LayeredUpdates()
        self.item_diamante = pygame.sprite.LayeredUpdates()
        self.item_bomba = pygame.sprite.LayeredUpdates()
        self.item_pocion = pygame.sprite.LayeredUpdates()

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
        vida_content = f"Vida: {Player.vida}"
        vida_surface = pygame.font.Font(None, 36).render(vida_content, True, Config.WHITE)
        vida_rect = vida_surface.get_rect()
        vida_rect.center = (2 * Config.TILESIZE, 21.5 * Config.TILESIZE)
        self.screen.blit(vida_surface, vida_rect)
        bomba_content = f"Bombas: {Player.bombas}"
        bomba_surface = pygame.font.Font(None, 36).render(bomba_content, True, Config.WHITE)
        bomba_rect = bomba_surface.get_rect()
        bomba_rect.center = (6 * Config.TILESIZE, 21.5 * Config.TILESIZE)
        self.screen.blit(bomba_surface, bomba_rect)
        diamante_content = f"Diamantes: {Player.diamantes}"
        diamante_surface = pygame.font.Font(None, 36).render(diamante_content, True, Config.WHITE)
        diamante_rect = diamante_surface.get_rect()
        diamante_rect.center = (11.5 * Config.TILESIZE, 21.5 * Config.TILESIZE)
        self.screen.blit(diamante_surface, diamante_rect)
        snorkel_content = f"Snorkel: {Player.traje}"
        snorkel_surface = pygame.font.Font(None, 36).render(snorkel_content, True, Config.WHITE)
        snorkel_rect = snorkel_surface.get_rect()
        snorkel_rect.center = (18 * Config.TILESIZE, 21.5 * Config.TILESIZE)
        self.screen.blit(snorkel_surface, snorkel_rect)
        pygame.display.update()

    def main(self):
        while self.playing:
            if sprites.Player.vida <= 0 or sprites.Player.diamantes == self.objetivoa:
                pygame.quit()
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
