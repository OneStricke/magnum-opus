import pygame
from src.game import apply_gravity
from src.physics import ObjectInSpace

earth = ObjectInSpace(300, 400, 1000, 0, 0)
asteroid = ObjectInSpace(700, 500, 1, -5, -20)

pygame.init()

# Set the height and width of the screen
size = [800, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")


done = False
clock = pygame.time.Clock()

while not done:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    screen.fill("white")

    pygame.draw.circle(screen, "blue", [earth.x_cog, earth.y_cog], 40)
    pygame.draw.circle(screen, "hotpink", [asteroid.x_cog, asteroid.y_cog], 20)

    apply_gravity(asteroid, earth, dt)

    pygame.display.flip()

pygame.quit()
