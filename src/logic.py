from src.physics import ObjectInSpace
import pygame
import src.constants as const
import numpy as np
from numba import jit
import math


def apply_gravity(movee: ObjectInSpace, mover: ObjectInSpace, dt):
    if movee.movable:
        force_x, force_y = mover.get_gravity_force(movee, const.G)
        movee.x_vel += force_x / movee.mass * dt
        movee.y_vel += force_y / movee.mass * dt


def apply_movement(movee, dt):
    movee.x_cog += movee.x_vel * dt
    movee.y_cog += movee.y_vel * dt


def boom(astr, screen, font_size):
    pygame.font.init()
    boom_font = pygame.font.SysFont('Comic Sans MS', font_size)
    surface = boom_font.render("BOOM!", False, 'Hotpink')
    screen.blit(surface, (astr.x_cog-font_size*2.5, astr.y_cog-font_size/2))


@jit(cache=True)
def dist_to_accel(dist_sq_aa, mass, diff_aa, G):
    dist_aa = np.sqrt(dist_sq_aa)
    mass_prod = mass[:, np.newaxis] * mass[np.newaxis, :]
    force_mag_aa = G * mass_prod / dist_sq_aa
    accel_aa = np.sum(
        (force_mag_aa / mass[:, np.newaxis])[:, :, np.newaxis]
        * (-diff_aa / dist_aa[:, :, np.newaxis]),
        axis=1)
    return accel_aa


@jit(cache=True)
def pos_to_dist(pos):
    diff_aa = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
    dist_sq_aa = np.sum(diff_aa ** 2, axis=2) + 0.0000001
    return diff_aa, dist_sq_aa


@jit(cache=True)
def math_earth(pos, mass, earth_pos, earth_mass, G):
    diff = earth_pos - pos
    dist_sq = np.sum(diff ** 2, axis=1) + 0.0000001
    dist = np.sqrt(dist_sq)
    force_mag = G * mass * earth_mass / dist_sq
    accel = (force_mag / mass)[:, np.newaxis] * (diff / dist[:, np.newaxis])
    return accel


def array_grav(asteroids, earth, dt):
    if not asteroids:
        return

    # pack everything ito arrays
    pos = np.array([[a.x_cog, a.y_cog] for a in asteroids], dtype=float)
    mass = np.array([a.mass for a in asteroids])

    # earth
    earth_mass = earth.mass
    earth_pos = np.array([earth.x_cog, earth.y_cog])
    accel = math_earth(pos, mass, earth_pos, earth_mass, const.G)
    for i, a in enumerate(asteroids):
        if a.movable:
            a.x_vel += float(accel[i, 0].real) * dt
            a.y_vel += float(accel[i, 1].real) * dt
            speed = math.sqrt(a.x_vel**2 + a.y_vel**2)
            if speed > 10000:
                a.x_vel = a.x_vel / speed * 10000
                a.y_vel = a.y_vel / speed * 10000

    # asteroids
    diff_aa, dist_sq_aa = pos_to_dist(pos)
    np.fill_diagonal(dist_sq_aa, np.inf)
    accel_aa = dist_to_accel(dist_sq_aa, mass, diff_aa, const.G)
    for i, a in enumerate(asteroids):
        if a.movable:
            a.x_vel += float(accel_aa[i, 0].real) * dt
            a.y_vel += float(accel_aa[i, 1].real) * dt
            speed = math.sqrt(a.x_vel**2 + a.y_vel**2)
            if speed > 10000:
                a.x_vel = a.x_vel / speed * 10000
                a.y_vel = a.y_vel / speed * 10000


def pre_load(earth, screen):
    astr = ObjectInSpace(200, 200, 1e5, 20, 0)
    astr = ObjectInSpace(300, 400, 1e5, 0, 0)
    for i in range(60):
        screen.fill("white")
        pygame.font.init()
        font = pygame.font.SysFont('Calibri', 100)
        surface = font.render("Loading...", False, 'hotpink')
        screen.blit(surface, (250, 250))
        pygame.display.flip()
        start_cycle([astr], earth, 16, screen, 1)


@jit(cache=True)
def aoa_hood(earth_x, earth_y, astr_x, astr_y, astr_vx, astr_vy):
    dx = astr_x - earth_x
    dy = astr_y - earth_y
    dist = math.sqrt(dx*dx + dy*dy)
    if dist == 0 or (astr_vx == 0 and astr_vy == 0):
        return 0.0
    nx, ny = dx/dist, dy/dist
    speed = math.sqrt(astr_vx**2 + astr_vy**2)
    dot = (astr_vx*nx + astr_vy*ny) / speed
    return abs(math.degrees(math.asin(max(-1.0, min(1.0, dot)))))


def aoa(earth, asteroid):
    return aoa_hood(earth.x_cog, earth.y_cog,
                    asteroid.x_cog, asteroid.y_cog,
                    asteroid.x_vel, asteroid.y_vel)


def start_cycle(asteroids, earth, dt, screen, font_size):

    array_grav(asteroids, earth, dt)

    to_remove = []
    for asteroid in asteroids:
        apply_movement(asteroid, dt)

        # collision
        if asteroid.is_collided(earth):
            if asteroid.movable:
                speed = math.sqrt(asteroid.x_vel**2 + asteroid.y_vel**2)
                angle = aoa(earth, asteroid)
                if speed == 0:
                    asteroid.pm = 0.1
                else:
                    speed_score = (math.sqrt(speed / 50)) ** 0.5
                    angle_score = (1 - angle / 90) ** 0.5
                    asteroid.pm *= speed_score * angle_score + 0.1
                const.points += 100*asteroid.pm

            if const.booming:
                boom(asteroid, screen, font_size)
            if not earth.movable:
                asteroid.movable = False
            asteroid.x_vel = 0
            asteroid.y_vel = 0
            font_size += 1
            if font_size >= 30:
                to_remove.append(asteroid)
                font_size = 1

        # deletion of far stuff
        out_of_x = asteroid.x_cog < -1000 or asteroid.x_cog > 1800
        out_of_y = asteroid.y_cog < -1000 or asteroid.y_cog > 1400
        if out_of_x or out_of_y:
            to_remove.append(asteroid)

    # correction of dealdly sin (deleting stuff from list while iterating)
    for asteroid in to_remove:
        if asteroid in asteroids:
            asteroids.remove(asteroid)
    return font_size
