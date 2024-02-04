import time

import pygame
from config import *
import math
from Character.MapLoader import *
import random


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(Config.BLACK)
        return sprite


class Player(pygame.sprite.Sprite):
    equip_time = 0
    last_damage_time = 0
    colisionado_x = False
    colisionado_y = False
    vida = 10
    bombas = 0
    diamantes = 0
    traje = False
    trajePuesto = False

    def __init__(self, game, x, y):

        self.game = game
        self._layer = Config.PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * Config.TILESIZE
        self.y = y * Config.TILESIZE
        self.width = Config.TILESIZE
        self.height = Config.TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(132, 80, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.collide_item_bomba('x')
        self.collide_item_diamante('x')
        self.collide_item_pocion('x')
        self.collide_item_snorkel('x')
        self.collide_water('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.collide_item_bomba('y')
        self.collide_item_diamante('y')
        self.collide_item_pocion('y')
        self.collide_item_snorkel('y')
        self.collide_water('y')
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x_change -= Config.PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += Config.PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= Config.PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += Config.PLAYER_SPEED
            self.facing = 'down'
        if keys[pygame.K_a]:
            self.x_change -= Config.PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            self.x_change += Config.PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            self.y_change -= Config.PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            self.y_change += Config.PLAYER_SPEED
            self.facing = 'down'
        if keys[pygame.K_e]:
            current_time = time.time()
            if (self.traje
                    and not self.trajePuesto
                    and current_time > (Player.equip_time + 1)):
                self.trajePuesto = True
                Player.equip_time = current_time
                Config.EQUIP_SOUND.play()
            elif (self.traje
                  and self.trajePuesto
                  and current_time > (Player.equip_time + 1)):
                self.trajePuesto = False
                Player.equip_time = current_time
                Config.EQUIP_SOUND.play()
        if keys[pygame.K_SPACE]:
            current_time = time.time()
            if Player.bombas > 0 and current_time > (Player.equip_time + 1):
                Player.equip_time = current_time
                Player.bombas -= 1
                Player.destroy_blocks_around(self)
        Config.PLAYER_SPEED = 3



    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits and not self.colisionado_x:
                self.colisionado_x = True
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    Player.vida -= 1
                    Config.AUCH_SOUND.play()
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    Player.vida -= 1
                    Config.AUCH_SOUND.play()
            elif hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
            elif not hits:
                self.colisionado_x = False
        elif direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits and not self.colisionado_y:
                self.colisionado_y = True
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    Player.vida -= 1
                    Config.AUCH_SOUND.play()
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    Player.vida -= 1
                    Config.AUCH_SOUND.play()
            elif hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
            elif not hits:
                self.colisionado_y = False


    def collide_item_bomba(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.item_bomba, False)
            for hit in hits:
                hit.kill()
                Player.bombas += 1
                Config.ITEMGRAB_SOUND.play()


        elif direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.item_bomba, False)
            for hit in hits:
                hit.kill()
                Player.bombas += 1
                Config.ITEMGRAB_SOUND.play()

    def collide_item_diamante(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.item_diamante, False)
            for hit in hits:
                hit.kill()
                Player.diamantes += 1
                Config.PICKUP_SOUND.play()


        elif direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.item_diamante, False)
            for hit in hits:
                hit.kill()
                Player.diamantes += 1
                Config.PICKUP_SOUND.play()

    def collide_item_pocion(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.item_pocion, False)
            for hit in hits:
                hit.kill()
                Player.vida += 3
                if Player.vida > 10:
                    Player.vida = 10
                Config.DRINK_SOUND.play()


        elif direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.item_pocion, False)
            for hit in hits:
                hit.kill()
                Player.vida += 3
                if Player.vida > 10:
                    Player.vida = 10
                    Config.DRINK_SOUND.play()


    def collide_item_snorkel(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.item_snorkel, False)
            for hit in hits:
                hit.kill()
                Player.traje = True
                Config.ITEMGRAB_SOUND.play()


        elif direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.item_snorkel, False)
            for hit in hits:
                hit.kill()
                Player.traje = True
                Config.ITEMGRAB_SOUND.play()

    def collide_water(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.water, False)
            if hits and not self.trajePuesto:
                current_time = time.time()
                if current_time - self.last_damage_time > 1:
                    Player.vida -= 3
                    self.last_damage_time = current_time
                    Config.DROWN_SOUND.play()
                    Config.PLAYER_SPEED = 1.5

        elif direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.water, False)
            if hits and not self.trajePuesto:
                current_time = time.time()
                if current_time - self.last_damage_time > 1:
                    Player.vida -= 3
                    self.last_damage_time = current_time
                    Config.DROWN_SOUND.play()
                    Config.PLAYER_SPEED = 1.5


    def destroy_blocks_around(self):
        for sprite in self.game.blocks:
            if (abs(sprite.rect.x - self.rect.x) <= 2 * Config.TILESIZE
                    and abs(sprite.rect.y - self.rect.y) <= 2 * Config.TILESIZE):
                sprite.kill()
            boom = Config.EXPLOSION_SOUND
            boom.set_volume(0.01)
            boom.play()


    def animate(self):
        if not self.trajePuesto:
            down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

            up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                             self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                             self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

            left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

            right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        else:
            down_animations = [self.game.character_spritesheet.get_sprite(104, 2, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(136, 2, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(168, 2, self.width, self.height)]

            up_animations = [self.game.character_spritesheet.get_sprite(104, 34, self.width, self.height),
                             self.game.character_spritesheet.get_sprite(136, 34, self.width, self.height),
                             self.game.character_spritesheet.get_sprite(168, 34, self.width, self.height)]

            left_animations = [self.game.character_spritesheet.get_sprite(104, 98, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(136, 98, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(168, 98, self.width, self.height)]

            right_animations = [self.game.character_spritesheet.get_sprite(104, 66, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(136, 66, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(168, 66, self.width, self.height)]
        if not self.trajePuesto:
            if self.facing == "down":
                if self.y_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
                else:
                    self.image = down_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1
            if self.facing == "up":
                if self.y_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
                else:
                    self.image = up_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "right":
                if self.x_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
                else:
                    self.image = right_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "left":
                if self.x_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
                else:
                    self.image = left_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1
        else:
            if self.facing == "down":
                if self.y_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(104, 2, self.width, self.height)
                else:
                    self.image = down_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1
            if self.facing == "up":
                if self.y_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(104, 34, self.width, self.height)
                else:
                    self.image = up_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "right":
                if self.x_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(104, 66, self.width, self.height)
                else:
                    self.image = right_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "left":
                if self.x_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(104, 98, self.width, self.height)
                else:
                    self.image = left_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = Config.BLOCK_LAYER

        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * Config.TILESIZE
        self.y = y * Config.TILESIZE
        self.width = Config.TILESIZE
        self.height = Config.TILESIZE

        self.image = pygame.image.load("assets/wall.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game

        self._layer = Config.GROUND_LAYER

        self.groups = self.game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * Config.TILESIZE
        self.y = y * Config.TILESIZE
        self.width = Config.TILESIZE
        self.height = Config.TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(400, 290, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Water(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = Config.BLOCK_LAYER

        self.groups = self.game.all_sprites, self.game.water
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * Config.TILESIZE
        self.y = y * Config.TILESIZE
        self.width = Config.TILESIZE
        self.height = Config.TILESIZE

        self.image = self.game.water_spritesheet.get_sprite(32, 32, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Diamante(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = Config.BLOCK_LAYER

        self.groups = self.game.all_sprites, self.game.item_diamante
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * Config.TILESIZE
        self.y = y * Config.TILESIZE
        self.width = Config.TILESIZE
        self.height = Config.TILESIZE

        self.image = pygame.image.load("assets/diamante.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Bomba(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = Config.BLOCK_LAYER

        self.groups = self.game.all_sprites, self.game.item_bomba
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * Config.TILESIZE
        self.y = y * Config.TILESIZE
        self.width = Config.TILESIZE
        self.height = Config.TILESIZE

        self.image = pygame.image.load("assets/bomba.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Pocion(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = Config.BLOCK_LAYER

        self.groups = self.game.all_sprites, self.game.item_pocion
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * Config.TILESIZE
        self.y = y * Config.TILESIZE
        self.width = Config.TILESIZE
        self.height = Config.TILESIZE

        self.image = pygame.image.load("assets/pocion.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Snorkel(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = Config.BLOCK_LAYER

        self.groups = self.game.all_sprites, self.game.item_snorkel
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * Config.TILESIZE
        self.y = y * Config.TILESIZE
        self.width = Config.TILESIZE
        self.height = Config.TILESIZE

        self.image = pygame.image.load("assets/snorkel.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
