import math


class ObjectInSpace:
    """general physical object class"""
    def __init__(self, x_cog, y_cog, mass, x_vel, y_vel, movable=True):
        self.x_cog = x_cog
        self.y_cog = y_cog
        self.mass = mass
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.movable = movable

    def get_gravity_force(self, other, GRAVITATIONAL: float):
        """returns force towords the mover from the movee in two axces

        Args:
            other (ObjectInSpace): mover
            GRAVITATIONAL (float): const

        Returns:
            tuple: (force_x, force_y) towords the movee
        """
        dist_x = self.x_cog - other.x_cog
        dist_y = self.y_cog - other.y_cog
        dist_sq = (self.x_cog - other.x_cog)**2 + (self.y_cog - other.y_cog)**2
        dist = math.sqrt(dist_sq)
        force = GRAVITATIONAL*self.mass*other.mass/dist_sq
        return (force * dist_x/dist, force * dist_y/dist)

    def sum_obj(*args):
        weighted_sum_x = 0
        weighted_sum_y = 0
        mass_sum = 0
        for i in range(len(args)):
            weighted_sum_x += args[i].mass * args[i].x_cog
            weighted_sum_y += args[i].mass * args[i].y_cog
            mass_sum += args[i].mass
        return (weighted_sum_x/mass_sum, weighted_sum_y/mass_sum)