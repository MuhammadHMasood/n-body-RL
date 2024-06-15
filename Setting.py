# An idea about code structure
# this is a class to represent a specific setup of an n-body problem
# It will store the full information, but will be able to convert it into
# various condensed forms suitable for machine learning
# Maybe we could also have a Chain class to hold a sequence of settings to have a complete simulation

import rebound
import numpy as np
from Planet import Planet
from Planet_old import Planet_old
from PlanetarySystem_old import PlanetarySystem_old



class Setting:
    def __init__(self, *planets, g=1, step=1, centered=False, scaled=False, g_removed=False, step_removed=False):
        self.g = g
        self.planets = list(planets)
        self.step = step
        self.centered = centered
        self.scaled = scaled
        self.g_removed = g_removed
        self.step_removed = step_removed

    def simulate(self):
        sim = rebound.Simulation()
        sim.G = self.g
        # sim.units = ('m', 's', 'kg')
        sim.units = ('yr', 'AU', 'Msun')
        sim.integrator = "leapfrog"
        sim.add(self.get_particles())
        op = rebound.OrbitPlot(sim)
        op.fig.savefig("orbit3.png")
        sim.integrate(self.step)
        

        planets = [Planet.load_particle(particle) for particle in sim.particles]
        return Setting(*planets, g=self.g, step=self.step, scaled=self.scaled, centered=self.centered, g_removed=self.g_removed, step_removed=self.step_removed)
    
    def simulate_old(self):
        planets_old = [planet.get_planet_old() for planet in self.planets]
        a = 100
        sim = PlanetarySystem_old(planets_old, self.g, a * self.step, 1/a)
        sim.run_animation()


    def get_vector(self, reduction_type="none", vector_type="pos_vel"):
        # will return the input vector with the maximum dimensional reduction
        match reduction_type:
            case "none":
                return NotImplemented

            case "partial":
                return NotImplemented

            case "full":
                return NotImplemented

    def get_planets(self):
        new_list = []
        for planet in self.planets:
            new_list.append(planet.copy())
        return new_list
    
    def reduce(self, centered=False, scaled=False, g_removed=False, step_removed=False):

        new_planets = self.get_planets()
        step = self.step
        g = self.g
        if centered:
            new_planets = self.reduce_center(new_planets)
        if scaled:
            new_planets = self.reduce_scale_orientation(new_planets)
        if g_removed:
            new_planets = self.reduce_g(new_planets)
            g = 1
        if step_removed:
            new_planets = self.reduce_step(new_planets)
            step = 1
        return Setting(*new_planets, g=g, step=step, centered=centered, scaled=scaled, g_removed=g_removed, step_removed=step_removed)
    
    def reintroduce(self, setting):
        new_planets = setting.get_planets()

        if setting.centered:
            new_planets = self.reintroduce_center(new_planets)
        if setting.scaled:
            new_planets = self.reintroduce_scale_orientation(new_planets)
        if setting.g_removed:
            new_planets = self.reintroduce_g(new_planets)
        if setting.step_removed:
            new_planets = self.reintroduce_step(new_planets)
        
        return Setting(*new_planets, g=self.g, step=self.step)



    def reduce_center(self, planets):
        momentum = np.array([0., 0.])
        mass = 0
        position = np.array([0., 0.])
        for planet in planets:
            momentum += planet.mass * planet.vel
            mass += planet.mass
            position += planet.mass * planet.pos

        for planet in planets:
            planet.vel -= momentum / mass
            planet.pos -= position / mass

        return planets


    def reintroduce_center(self, planets):
        momentum = np.array([0., 0.])
        mass = 0
        position = np.array([0., 0.])
        for planet in self.planets:
            momentum += planet.mass * planet.vel
            mass += planet.mass
            position += planet.mass * planet.pos

        for planet in planets:
            planet.vel += momentum / mass
            planet.pos += position / mass

        return planets


    def reduce_g(self, planets):
        for planet in planets:
            planet.mass *= self.g
        return planets


    def reintroduce_g(self, planets):
        for planet in planets:
            planet.mass /= self.g
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

        det = np.linalg.det(matrix)

        matrix = matrix / det

        for planet in planets:
            planet.pos = matrix.dot(planet.pos)
            planet.vel = matrix.dot(planet.vel)
            planet.mass *= det**(3/2)

        return planets


    def reintroduce_scale_orientation(self, planets):
        matrix = np.array([[self.planets[0].pos[0], -self.planets[0].pos[1]],
                        [self.planets[0].pos[1], self.planets[0].pos[0]]])

        det = np.linalg.det(matrix)

        for planet in planets:
            planet.pos = matrix.dot(planet.pos)
            planet.vel = matrix.dot(planet.vel)
            planet.mass *= det**(3/2)

        return planets
    
    def get_particles(self):
        return [planet.get_particle() for planet in self.planets]


    def __repr__(self):
        return str(self.planets)
        