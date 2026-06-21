import math


class ObjectInSpace:
    """general physical object class"""
    def __init__(self, x_cog, y_cog,
                 mass, x_vel, y_vel,
                 movable=True, radius=1, pm=1):
        self.x_cog = x_cog
        self.y_cog = y_cog
        self.mass = mass
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.movable = movable
        self.radius = radius
        self.pm = pm

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
        dist_sq = (self.x_cog-other.x_cog)**2+(self.y_cog-other.y_cog)**2
        dist = math.sqrt(dist_sq)
        try:
            force = GRAVITATIONAL*self.mass*other.mass/dist_sq
            return (force * dist_x/dist, force * dist_y/dist)
        except ZeroDivisionError:
            return (0, 0)

    def dist(self, other):
        dist_sq = (self.x_cog - other.x_cog)**2 + (self.y_cog - other.y_cog)**2
        return math.sqrt(dist_sq)

    def sum_obj(*args):
        weighted_sum_x = 0
        weighted_sum_y = 0
        mass_sum = 0
        for i in range(len(args)):
            weighted_sum_x += args[i].mass * args[i].x_cog
            weighted_sum_y += args[i].mass * args[i].y_cog
            mass_sum += args[i].mass
        weight_x = weighted_sum_x/mass_sum
        weight_y = weighted_sum_y/mass_sum
        return ObjectInSpace(weight_x, weight_y, mass_sum, 0, 0, False)

    def is_collided(self, other):
        if self.radius + other.radius >= self.dist(other):
            return True
        else:
            return False
