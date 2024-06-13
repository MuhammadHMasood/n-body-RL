# An idea about code structure
# this is a class to represent a specific setup of an n-body problem
# It will store the full information, but will be able to convert it into
# various condensed forms suitable for machine learning
# Maybe we could also have a Chain class to hold a sequence of settings to have a complete simulation

import rebound
import numpy as np
from Planet import Planet


class Setting:
    def __init__(self, g, step, *planets):
        self.g = g
        self.planets = list(planets)
        self.step = step

    def simulate(self):
        # will use the library to give the "perfect" prediction
        return NotImplemented

    def get_vector(self, reduction_type="partial", vector_type="pos_vel"):
        # will return the input vector with the maximum dimensional reduction
        match
        reduction_type:
        case
        "non":
        return NotImplemented

    case
    "partial":
    return NotImplemented


case
"full":
return NotImplemented


def reduce_center(self, planets):
    momentum = np.array([0, 0])
    mass = 0
    position = np.array([0, 0])
    for planet in planets:
        momentum += planet.mass * planet.vel
        mass += planet.mass
        position += planet.mass * planet.pos

    for planet in planets:
        planet.vel -= momentum / mass
        planet.pos -= position / mass

    return planets


def reintroduce_center(self, planets):
    momentum = np.array([0, 0])
    mass = 0
    position = np.array([0, 0])
    for planet in self.planets:
        momentum += planet.mass * planet.vel
        mass += planet.mass
        position += planet.mass * planet.pos

    for planet in planets:
        planet.vel += momentum / mass
        planet.pos += position / mass

    return planets


def reduce_g(self, planets):
    sqrt_g = np.sqrt(self.g)
    for planet in planets:
        planet.mass *= sqrt_g
    return planets


def reintroduce_g(self, planets):
    sqrt_g = np.sqrt(self.g)
    for planet in planets:
        planet.mass /= sqrt_g
    return planets


def reduce_step(self, planets):
    sqrt_step = np.sqrt(self.step)
    for planet in planets:
        planet.vel *= self.step
        planet.mass *= sqrt_step
    return planets


def reintroduce_step(self, planets):
    sqrt_step = np.sqrt(self.step)
    for planet in planets:
        planet.vel /= self.step
        planet.mass /= sqrt_step
    return planets


def reduce_scale_orientation(self, planets):
    matrix = np.array([[planets[0].pos[0], planets[0].pos[1]],
                       [-planets[0].pos[1], planets[0].pos[0]]])

    det_squared = np.linalg.det(matrix)

    matrix = matrix / det_squared

    for planet in planets:
        planet.pos = matrix.dot(planet.pos)
        planet.vel = matrix.dot(planet.vel)
        planet.mass /= det_squared

    return planets


def reintroduce_scale_orientation(self, planets):
    matrix = np.array([[self.planets[0].pos[0], -self.planets[0].pos[1]],
                       [self.planets[0].pos[1], self.planets[0].pos[0]]])

    det_squared = np.linalg.det(matrix)

    for planet in planets:
        planet.pos = matrix.dot(planet.pos)
        planet.vel = matrix.dot(planet.vel)
        planet.mass *= det_squared

    return planets


def __repr__(self):
    return str(self.planets)


def get_list(self):
    new_list = []
    for planet in self.planets:
        new_list.append(planet.copy())
    return new_list


planet1 = Planet(1, np.array([1, 1]), np.array([0, 1]))
planet2 = Planet(1, np.array([-1, -1]), np.array([0, -1]))
setting = Setting(1, 1, planet1, planet2)
print(setting.reduce_scale_orientation(setting.get_list()))
print(setting.planets)
