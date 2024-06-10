import numpy as np


class Planet:
    """
    represents a planet that affects other with its gravity and is affected by the gravity of others
    """
    def __init__(self, mass, position, velocity, name="unnamed", colour=(0, 0, 0)):
        self.mass = mass
        self.pos = position
        self.pos_old = position
        self.vel = velocity
        self.name = name
        self.acc = 0
        self.acc_old = 0
        self.force = 0
        self.colour = colour
        self.potential = 0

    def update_euler(self, time_step):
        """
        makes all the changes necessary for a single timestep using euler integration
        """
        self.pos_old = self.pos

        self.acc_old = self.acc

        self.acc = self.force / self.mass

        self.pos = self.pos + self.vel * time_step

        self.vel += self.acc * time_step

    def update_position_beeman(self, time_step):
        """
        updates the position of the planet according to beeman integration and stores the previous position
        """
        self.pos_old = self.pos
        self.pos = self.pos + self.vel * time_step + (self.acc / 2 + (self.acc - self.acc_old) / 6) * time_step ** 2

    def update_velocity_beeman(self, time_step):
        """
        updates the velocity of the planet according to beeman integration and stores the previous position
        """
        new_acc = self.force / self.mass
        self.vel = self.vel + (2*new_acc+5*self.acc-self.acc_old)*time_step / 6
        self.acc_old = self.acc
        self.acc = new_acc

    def get_kinetic_energy(self):
        """
        returns the kinetic energy of the planet
        """
        return self.mass * np.dot(self.vel, self.vel) / 2

    def __str__(self):
        # return f"{self.name} at {self.pos}, with speed {self.vel} and velocity {self.vel}"
        return self.name

    def add_force(self, force):
        """
        adds a force to the planets total force
        """
        self.force += force

    def add_potential(self, potential):
        """
        adds a potential to the planets total gravitational potential
        """
        self.potential += potential
