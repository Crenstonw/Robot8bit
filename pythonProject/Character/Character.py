import pygame

from Main import screen
class Character():
    def __init__ (self, pos_x, pos_y):
        self.x, self.y = pos_x, pos_y
        self.character_image = pygame.image.load("assets/character.png")

    def print(self):
        screen.blit(self.character_image, (self.x, self.y))
