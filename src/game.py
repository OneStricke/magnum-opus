from src.physics import ObjectInSpace

earth = ObjectInSpace(300, 400, 1, 0, 0)
G = 10


def apply_gravity(movee: ObjectInSpace, mover: ObjectInSpace, dt):
    force_x, force_y = mover.get_gravity_force(movee, G)
    movee.x_vel += force_x / movee.mass
    movee.y_vel += force_y / movee.mass
    movee.x_cog += movee.x_vel * dt
    movee.y_cog += movee.y_vel * dt

# # Check impact
# if earth.check_collision(asteroid.pos, asteroid.radius):
#     # award points, trigger explosion, etc.
#     pass
