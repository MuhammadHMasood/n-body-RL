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
        self.acc = numpy.array([0,0])

    def return_particle(self):
        return rebound.Particle(m=self.mass, x=self.pos[0], y=self.pos[1], vx=self.vel[0], vy=self.vel[1])

    def return_vector(self, type):
        match type:
            case "1":
                return np.concatenate(self.pos, self.vel)
            case



