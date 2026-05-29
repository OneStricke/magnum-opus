import math


class ObjectInSpace:
    """general physical object class"""
    def __init__(self, x_cog, y_cog,
                 mass, x_vel, y_vel,
                 movable=True, radius=1):
        self.x_cog = x_cog
        self.y_cog = y_cog
        self.mass = mass
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.movable = movable
        self.radius = radius

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

# inspired by https://github.com/alessialin/BarnesHut-py.git
# shoud prolly split into diffrent files like original


class QuadTree:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.body = None
        self.mass_center = None
        self.subs = []

    def in_bounds(self, obj):
        return (self.x <= obj.x_cog < self.x + self.width and
                self.y <= obj.y_cog < self.y + self.height)

    def subdivide(self):
        hw = self.width / 2
        hh = self.height / 2
        self.subs = [
            QuadTree(self.x,      self.y,      hw, hh),  # NW
            QuadTree(self.x + hw, self.y,      hw, hh),  # NE
            QuadTree(self.x,      self.y + hh, hw, hh),  # SW
            QuadTree(self.x + hw, self.y + hh, hw, hh)]  # SE

    def get_sub(self, obj):
        for sub in self.subs:
            if sub.in_bounds(obj):
                return sub
        return None

    def insert(self, obj):
        if self.mass_center is None:
            self.mass_center = obj
        else:
            self.mass_center = ObjectInSpace.sum_obj(self.mass_center, obj)

        # Empty leaf
        if self.body is None and self.subs is None:
            self.body = obj
            return

        if self.subs is not None:
            child = self.get_sub(obj)
            if child:
                child.insert(obj)
            return

        self.subdivide()

        old = self.body
        self.body = None

        for o in (old, obj):
            child = self.get_sub(o)
            if child:
                child.insert(o)

    def get_force(self, obj, G, theta=0.5):
        if self.mass_center is None:
            return (0, 0)

        if self.body is obj:
            return (0, 0)

        if self.subs is None:
            if self.body is not None and self.body is not obj:
                return self.body.get_gravity_force(obj, G)
            return (0, 0)

        s = self.width
        d = obj.dist(self.mass_center)

        if d == 0:
            return (0, 0)

        if s / d < theta:
            return self.mass_center.get_gravity_force(obj, G)

        fx, fy = 0, 0
        for sub in self.subs:
            sfx, sfy = sub.get_force(obj, G, theta)
            fx += sfx
            fy += sfy
        return (fx, fy)
