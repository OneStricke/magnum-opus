from src.physics import ObjectInSpace

G = 10


def apply_gravity(movee: ObjectInSpace, mover: ObjectInSpace, dt):
    force_x, force_y = mover.get_gravity_force(movee, G)
    movee.x_vel += force_x / movee.mass
    movee.y_vel += force_y / movee.mass
    movee.x_cog += movee.x_vel * dt
    movee.y_cog += movee.y_vel * dt


def astr_click(x, y):
    return ObjectInSpace(x, y, 2, -22, -15)

# # Check impact
# if earth.check_collision(asteroid.pos, asteroid.radius):
#     # award points, trigger explosion, etc.
#     pass
