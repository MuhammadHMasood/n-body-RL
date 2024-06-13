import numpy as np
import rebound


class Planet:
    """
    represents a planet that affects other with its gravity and is affected by the gravity of others
    """
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.pos = position
        self.vel = velocity
        self.acc = np.array([0,0])

    def return_particle(self):
        return rebound.Particle(m=self.mass, x=self.pos[0], y=self.pos[1], vx=self.vel[0], vy=self.vel[1])

    def return_vector(self, type):
        match type:
            case "pos_vel":
                return np.concatenate(self.pos, self.vel)
            case "pos_vel_acc":
                return np.concatenate(self.pos, self.vel, self.acc)

    def __repr__(self):
        return f"pos={self.pos}, vel={self.vel}"

    def __str__(self):
        return f"pos={self.pos}, vel={self.vel}"

    def copy(self):
        new_planet = Planet(self.mass, self.pos.copy(), self.vel.copy())
        new_planet.acc = self.acc.copy()
        return new_planet

