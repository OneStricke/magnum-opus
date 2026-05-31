import pygame
from src.logic import astr_click, pre_load
from src.logic import start_cycle
from src.physics import ObjectInSpace
from src.settings import sett

asteroids = []
earth = ObjectInSpace(300, 400, 1e14, 0, 0, False, 40)
font_size = 1

pygame.init()

start = False

# Set the height and width of the screen
size = [800, 600]
screen = pygame.display.set_mode(size)

pre_load(earth, screen)

pygame.display.set_caption("Magnum Opus")


done = False
clock = pygame.time.Clock()

while not done:
    dt = clock.tick_busy_loop(60) / 1000.0  # tick(60)

    for event in pygame.event.get():  # User did something

        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mou, y_mou = pygame.mouse.get_pos()
            if x_mou <= 200 and x_mou >= 150 and y_mou <= 30 and y_mou >= 10:
                start = not start
            elif 780 <= x_mou <= 800 and 0 <= y_mou <= 20:
                start = False
                sett(screen)
            else:
                asteroids.append(astr_click(x_mou, y_mou))

    screen.fill("white")

    pygame.draw.circle(screen, "blue",
                       [earth.x_cog, earth.y_cog],
                       earth.radius)

    if start:
        font_size = start_cycle(asteroids, earth, dt, screen, font_size)

    for asteroid in asteroids:
        pygame.draw.circle(screen, "hotpink",
                           [asteroid.x_cog, asteroid.y_cog],
                           asteroid.radius)

    # fps
    pygame.font.init()
    font = pygame.font.SysFont('Calibri', 12)
    surface = font.render(str(int(clock.get_fps())), False, 'dark green')
    screen.blit(surface, (10, 10))

    # amount of asteroids
    surface1 = font.render(str(len(asteroids)), False, 'blue')
    screen.blit(surface1, (700, 10))

    # buttons
    pygame.draw.rect(screen, (0, 0, 0), [150, 10, 50, 20])
    pygame.draw.rect(screen, "red", [780, 0, 20, 20])

    pygame.display.flip()

pygame.quit()
