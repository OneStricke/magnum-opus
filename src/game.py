from src.physics import ObjectInSpace
import pygame
import random
import src.constants as const
import numpy as np
from numba import njit


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
                                        int(const.max_astr_mass))*1e5,
                         20, 0)


def boom(astr, screen, font_size):
    pygame.font.init()
    boom_font = pygame.font.SysFont('Comic Sans MS', font_size)
    surface = boom_font.render("BOOM!", False, 'Hotpink')
    screen.blit(surface, (astr.x_cog-font_size*2.5, astr.y_cog-font_size/2))


@njit
def mathing_grav(dist_sq_aa, mass, diff_aa):
    dist_aa = np.sqrt(dist_sq_aa)
    mass_prod = mass[:, np.newaxis] * mass[np.newaxis, :]
    force_mag_aa = const.G * mass_prod / dist_sq_aa
    accel_aa = np.sum(
        (force_mag_aa / mass[:, np.newaxis])[:, :, np.newaxis]
        * (-diff_aa / dist_aa[:, :, np.newaxis]),
        axis=1)
    return accel_aa


def array_grav(asteroids, earth, dt):
    if not asteroids:
        return

    # pack everything ito arrays
    pos = np.array([[a.x_cog, a.y_cog] for a in asteroids], dtype=float)
    mass = np.array([a.mass for a in asteroids])

    # earth
    earth_pos = np.array([earth.x_cog, earth.y_cog])
    diff = earth_pos - pos
    dist_sq = np.sum(diff ** 2, axis=1) + 0.0000001
    dist = np.sqrt(dist_sq)
    force_mag = const.G * mass * earth.mass / dist_sq
    accel = (force_mag / mass)[:, np.newaxis] * (diff / dist[:, np.newaxis])
    for i, a in enumerate(asteroids):
        if a.movable:
            a.x_vel += accel[i, 0] * dt
            a.y_vel += accel[i, 1] * dt

    # asteroids
    diff_aa = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
    dist_sq_aa = np.sum(diff_aa ** 2, axis=2) + 0.0000001
    np.fill_diagonal(dist_sq_aa, np.inf)

    # dist_aa = np.sqrt(dist_sq_aa)
    # mass_prod = mass[:, np.newaxis] * mass[np.newaxis, :]
    # force_mag_aa = const.G * mass_prod / dist_sq_aa
    # accel_aa = np.sum(
    #     (force_mag_aa / mass[:, np.newaxis])[:, :, np.newaxis]
    #     * (-diff_aa / dist_aa[:, :, np.newaxis]),
    #     axis=1)
    accel_aa = mathing_grav(dist_sq_aa, mass, diff_aa)
    for i, a in enumerate(asteroids):
        if a.movable:
            a.x_vel += accel_aa[i, 0] * dt
            a.y_vel += accel_aa[i, 1] * dt
