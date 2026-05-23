import math


class ObjectInSpace:
    """general physical object class"""
    def __init__(self, x_cog, y_cog, mass, x_vel, y_vel):
        self.x_cog = x_cog
        self.y_cog = y_cog
        self.mass = mass
        self.x_vel = x_vel
        self.y_vel = y_vel

    def get_gravity_force(self, other, GRAVITATIONAL):
        dist_x = self.x_cog - other.x_cog
        dist_y = self.y_cog - other.y_cog
        dist_sq = (self.x_cog - other.x_cog)**2 + (self.y_cog - other.y_cog)**2
        dist = math.sqrt(dist_sq)
        force = GRAVITATIONAL*self.mass*other.mass/dist_sq
        return (force * dist_x/dist, force * dist_y/dist)
