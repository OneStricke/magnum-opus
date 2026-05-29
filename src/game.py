from src.physics import ObjectInSpace
import pygame
import random
import src.constants as const


def apply_gravity(movee: ObjectInSpace, mover: ObjectInSpace, dt):
    if movee.movable:
        force_x, force_y = mover.get_gravity_force(movee, const.G)
        movee.x_vel += force_x / movee.mass * dt
        movee.y_vel += force_y / movee.mass * dt


def apply_movement(movee, dt):
    movee.x_cog += movee.x_vel * dt
    movee.y_cog += movee.y_vel * dt


def astr_click(x, y):
    return ObjectInSpace(x, y,
                         random.randint(int(const.min_astr_mass),
                                        int(const.max_astr_mass))*1e11,
                         40, 0)


def boom(astr, screen, font_size):
    pygame.font.init()
    boom_font = pygame.font.SysFont('Comic Sans MS', font_size)
    surface = boom_font.render("BOOM!", False, 'Hotpink')
    screen.blit(surface, (astr.x_cog-font_size*2.5, astr.y_cog-font_size/2))
