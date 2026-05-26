import pygame
from src.game import apply_gravity, astr_click, boom
from src.physics import ObjectInSpace

earth = ObjectInSpace(300, 400, 10**(14), 0, 0, False, 40)
asteroids = []
font_size = 1

pygame.init()

start = False

# Set the height and width of the screen
size = [800, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")


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
            else:
                asteroids.append(astr_click(x_mou, y_mou))

    screen.fill("white")

    pygame.draw.circle(screen, "blue",
                       [earth.x_cog, earth.y_cog],
                       earth.radius)

    if start:
        for asteroid in asteroids:
            pygame.draw.circle(screen, "hotpink",
                               [asteroid.x_cog, asteroid.y_cog],
                               asteroid.radius)
            apply_gravity(asteroid, earth, dt)
            for asteroid_mover in asteroids:
                if asteroid_mover is not asteroid:
                    apply_gravity(asteroid, asteroid_mover, dt)

            if asteroid.is_collided(earth):  # shit
                if font_size != 0:
                    boom(asteroid, screen, font_size)
                    if not earth.movable:
                        asteroid.movable = False
                    asteroid.x_vel = 0
                    asteroid.y_vel = 0
                    font_size += 1
                    if font_size >= 30:
                        asteroids.remove(asteroid)
                        font_size = 1

            out_of_x = asteroid.x_cog < -1000 or asteroid.x_cog > 1800
            out_of_y = asteroid.y_cog < -1000 or asteroid.y_cog > 1400
            if out_of_x or out_of_y:
                asteroids.remove(asteroid)

    pygame.font.init()
    font = pygame.font.SysFont('Calibri', 12)
    surface = font.render(str(int(clock.get_fps())), False, 'dark green')
    screen.blit(surface, (10, 10))

    pygame.draw.rect(screen, (0, 0, 0), [150, 10, 50, 20])
    pygame.display.flip()

pygame.quit()
