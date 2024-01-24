import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 736)) #80x45 casillas a 16 bits
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(16, 16)
player_radious = 16

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    #pygame.draw.line(color="white", start_pos= (0, 32), end_pos= (0, 720), width= )

    pygame.draw.circle(screen, "red", player_pos, player_radious)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_pos.y > player_radious*2:
        player_pos.y -= 32
    if keys[pygame.K_DOWN] and player_pos.y < (screen.get_height() - (player_radious*2)):
        player_pos.y += 32
    if keys[pygame.K_LEFT] and player_pos.x > player_radious*2:
        player_pos.x -= 32
    if keys[pygame.K_RIGHT] and player_pos.x < (screen.get_width()-(player_radious*2)):
        player_pos.x += 32

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()