import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 736)) #40x23 casillas a 16 bits
clock = pygame.time.Clock()
running = True
dt = 0

#Carga de sprites
sprite_width, sprite_height = 32, 32
sprite_image = pygame.image.load("assets/wall.png")
character_image = pygame.image.load("assets/character.png")

background_array = [[sprite_image for _ in range(23)] for _ in range(40)]

player_pos = pygame.Vector2(16, 16)
player_radius = 16
cell_size = 32
delay_time = 200

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for col in range(23):
        for row in range(40):
            x, y = row * sprite_width, col * sprite_height
            screen.blit(background_array[row][col], (x, y))

    #pygame.draw.line(color="white", start_pos= (0, 32), end_pos= (0, 720), width= )

    pygame.transform.scale(character_image, (32, 32))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_pos.y > player_radius * 2:
        player_pos.y -= 32
        pygame.time.delay(delay_time)
    if keys[pygame.K_DOWN] and player_pos.y < (screen.get_height() - (player_radius * 2)):
        player_pos.y += 32
        pygame.time.delay(delay_time)
    if keys[pygame.K_LEFT] and player_pos.x > player_radius * 2:
        player_pos.x -= 32
        pygame.time.delay(delay_time)
    if keys[pygame.K_RIGHT] and player_pos.x < (screen.get_width() - (player_radius * 2)):
        player_pos.x += 32
        pygame.time.delay(delay_time)

    pygame.display.flip()

    dt = clock.tick(120) / 1000

pygame.quit()
