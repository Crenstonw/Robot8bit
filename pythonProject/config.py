import pygame.mixer


class Config:
    pygame.mixer.init()
    AUCH_SOUND = pygame.mixer.Sound('assets/auch_sound.mp3')
    EQUIP_SOUND = pygame.mixer.Sound('assets/item-equip.mp3')
    PICKUP_SOUND = pygame.mixer.Sound('assets/pick_up.mp3')
    EXPLOSION_SOUND = pygame.mixer.Sound('assets/explosion.mp3')
    DRINK_SOUND = pygame.mixer.Sound('assets/drink.mp3')
    ITEMGRAB_SOUND = pygame.mixer.Sound('assets/grab.mp3')
    DROWN_SOUND = pygame.mixer.Sound('assets/drown.mp3')
    BACKGROUND_MUSIC =pygame.mixer.music
    BACKGROUND_MUSIC.load('assets/gamemusic.mp3')
    BACKGROUND_MUSIC.play(-1)
    BACKGROUND_MUSIC.set_volume(0.5)
    WIN_WIDTH = 1280
    WIN_HEIGHT = 704
    TILESIZE = 32
    FPS = 60

    PLAYER_LAYER = 3
    BLOCK_LAYER = 2
    GROUND_LAYER = 1

    PLAYER_SPEED = 3

    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)

    maptile = []
