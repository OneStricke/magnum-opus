import pygame
from src.game import apply_gravity, astr_click
from src.physics import ObjectInSpace

earth = ObjectInSpace(300, 400, 1000, 0, 0)
# asteroid = ObjectInSpace(700, 500, 1, -5, -20)

pygame.init()

start = False

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
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mou, y_mou = pygame.mouse.get_pos()
            if x_mou <= 200 and x_mou >= 150 and y_mou <= 30 and y_mou >= 10:
                start = True 
            else:
                astr1 = astr_click(x_mou, y_mou)

    screen.fill("white")

    pygame.draw.circle(screen, "blue", [earth.x_cog, earth.y_cog], 40)

    if start:
        pygame.draw.circle(screen, "hotpink", [astr1.x_cog, astr1.y_cog], 2)
        apply_gravity(astr1, earth, dt)

    pygame.draw.rect(screen, (0, 0, 0), [150, 10, 50, 20])
    pygame.display.flip()

pygame.quit()
