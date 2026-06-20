import pygame
import os
from src.logic import pre_load
from src.logic import start_cycle
from src.physics import ObjectInSpace
from src.settings import sett
import src.constants as const
import random


def load_texture(name):
    """Load assets/<name>.png as-is. Returns None if file doesn't exist."""
    path = os.path.join("assets", f"{name}.png")
    if not os.path.exists(path):
        return None
    return pygame.image.load(path).convert_alpha()


def draw_object(screen, obj, texture, color, fallback_radius=None):
    x, y = int(obj.x_cog), int(obj.y_cog)
    r = fallback_radius if fallback_radius is not None else obj.radius
    if texture is not None:
        scaled = pygame.transform.smoothscale(texture, (r * 2, r * 2))
        screen.blit(scaled, (x - r, y - r))
    else:
        pygame.draw.circle(screen, color, (x, y), r)


asteroids = []
earth = ObjectInSpace(300, 400, 1e14, 0, 0, False, 40)
font_size = 1
drag_start = None

pygame.init()

start = False

# Set the height and width of the screen
size = [800, 600]
screen = pygame.display.set_mode(size)

pre_load(earth, screen)

pygame.display.set_caption("Magnum Opus")

# load raw textures once
earth_tex = load_texture("earth")

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
                drag_start = (x_mou, y_mou)

        if event.type == pygame.MOUSEBUTTONUP and drag_start is not None:
            x_mou, y_mou = pygame.mouse.get_pos()
            vx = (drag_start[0] - x_mou) * 0.5
            vy = (drag_start[1] - y_mou) * 0.5
            for i in range(100):
                asteroids.append(ObjectInSpace(
                    drag_start[0] + random.randint(-5, 5),
                    drag_start[1] + random.randint(-5, 5),
                    random.randint(int(const.min_astr_mass),
                                   int(const.max_astr_mass)) * 1e5,
                    vx + random.randint(-2, 2),
                    vy + random.randint(-2, 2),
                    ))
            drag_start = None

    screen.fill("grey")

    draw_object(screen, earth, earth_tex, "blue", earth.radius)

    if start:
        font_size = start_cycle(asteroids, earth, dt, screen, font_size)

    for asteroid in asteroids:
        pygame.draw.circle(screen, "hotpink",
                           [asteroid.x_cog, asteroid.y_cog],
                           asteroid.radius)

    # slingshot line
    if drag_start is not None:
        x_cur, y_cur = pygame.mouse.get_pos()
        pygame.draw.line(screen, "red", drag_start, (x_cur, y_cur), 2)

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
