from src.physics import ObjectInSpace
import pygame

G = 10**(-9)


def apply_gravity(movee: ObjectInSpace, mover: ObjectInSpace, dt):
    if movee.movable:
        force_x, force_y = mover.get_gravity_force(movee, G)
        movee.x_vel += force_x / movee.mass * dt
        movee.y_vel += force_y / movee.mass * dt


def apply_movement(movee, dt):
    movee.x_cog += movee.x_vel * dt
    movee.y_cog += movee.y_vel * dt


def astr_click(x, y):
    return ObjectInSpace(x, y, 100000000000, 10, 0)


def boom(astr, screen, font_size):
    pygame.font.init()
    boom_font = pygame.font.SysFont('Comic Sans MS', font_size)
    surface = boom_font.render("BOOM!", False, 'Hotpink')
    screen.blit(surface, (astr.x_cog-font_size*2.5, astr.y_cog-font_size/2))
