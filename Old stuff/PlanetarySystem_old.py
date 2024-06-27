import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Planet_old import Planet_old


class PlanetarySystem_old:
    """
    represents the solar systems, handles simulation and animation
    """
    def __init__(self, planets, g, limit, step, integrator="beeman"):

        # simulation parameters
        self.limit = limit  # the maximum number of iteration
        self.step = step  # the duration of one timestep
        self.g = g  # the graviational constant

        # list for planets
        self.planets = planets
        self.total_time = 0  # stores the total time
        self.potential_energy = 0  # stores the potential energy

        # selects the appropriate type of integration based on the input
        if integrator == "beeman":
            self.perform_step = getattr(self, "perform_step_beeman")
        elif integrator == "euler":
            self.perform_step = getattr(self, "perform_step_euler")

    def run_simulation(self):
        """
        executes a simulation without any animation
        """
        # initialization necessary beeman integration
        self.update_forces()
        for planet in self.planets:
            planet.acc = planet.force / planet.mass
            planet.acc_old = planet.acc

        # runs the simulation for the specified time
        while self.total_time < self.limit * self.step:
            self.perform_step()
        
        return self.planets

    def perform_step_beeman(self):
        """
        performs one step using beeman integration
        """

        self.potential_energy = 0
        # first the position of each planet is updated
        for planet in self.planets:
            planet.update_position_beeman(self.step)

        # then the new acceleration is calculated and the velocity is updates
        self.update_forces()
        for planet in self.planets:
            planet.update_velocity_beeman(self.step)

        self.total_time += self.step

    def perform_step_euler(self):
        """
        performs one step using euler integration
        """

        self.potential_energy = 0
        self.update_forces()

        for planet in self.planets:
            planet.update_euler(self.step)

        # the total energy is stored

        self.total_time += self.step

    def update_forces(self):
        """
        calculates the force applied to each planet
        """
        for planet in self.planets:
            planet.force = 0
            planet.potential = 0
        for i, planet1 in enumerate(self.planets):
            # the second for loop integrates only through the planets that come after planet1 to prevent double counting
            for planet2 in self.planets[i+1:]:
                self.add_force_pair(planet1, planet2)

    def add_force_pair(self, planet1, planet2):
        """
        for a given pair of planets, calculates the force on each planet
        and updates the each planets' and the system's gravitational potential energy
        """
        dist_vec = planet2.pos - planet1.pos  # the distance between the two planets
        dist_square = dist_vec @ dist_vec
        mag_dist = np.sqrt(dist_square)

        # updates the planets' and the system's potential
        potential = -self.g * planet1.mass * planet2.mass / mag_dist
        planet1.add_potential(potential)
        planet2.add_potential(potential)
        self.potential_energy += potential

        # adds the force on each planet
        planet1.add_force(-dist_vec * potential / dist_square)
        planet2.add_force(dist_vec * potential / dist_square)

    def run_animation(self):
        """
        initializes and runs simulation concurrantly with an animation
        """

        max_orb = 10

        # creates a circular patch coreesponding to each planet
        self.patches = []

        for planet in self.planets:
            print(planet)
            self.patches.append(plt.Circle(planet.pos, max_orb * 0.02, animated=True))

        # create plot elements
        plt.style.use('dark_background')
        fig = plt.figure()
        ax = plt.axes()

        for i in self.patches:
            ax.add_patch(i)

        # set up the axes
        lim = max_orb
        ax.axis("scaled")
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)

        # create the animator
        self.anim = FuncAnimation(fig, self.animate, frames=self.limit, repeat=False, interval=10, blit=True)

        # initialization of beeman integration
        self.update_forces()
        for planet in self.planets:
            planet.acc = planet.force / planet.mass
            planet.acc_old = planet.acc

        # show the plot
        plt.show()

    def animate(self, i):
        """
        performs one step in the animation
        """

        self.perform_step()

        for i, v in enumerate(self.planets):
            self.patches[i].center = v.pos


        return self.patches

    def simulate_to_file(self, filename):
        """
        initializes and runs the simulation, and saves the position of the planets o file in each iteration
        """
        fileout = open(filename, "w")
        fileout.write("# each column represent the position of each planet in each timestep\n")
        fileout.write("# the first row contains the colors of the planets in each row\n")
        # write to file the colours of all the planets
        for planet in self.planets[:-1]:
            fileout.write(f"{planet.colour},")
        fileout.write(f"{self.planets[-1].colour}\n")

        # initializes the planets acceleration
        self.update_forces()
        for planet in self.planets:
            planet.acc = planet.force / planet.mass
            planet.acc_old = planet.acc

        # runs the simulation for the specified time
        while self.total_time < self.limit * self.step:
            self.perform_step()
            # writes to file the positions of all the planets
            for planet in self.planets[:-1]:
                fileout.write(f"{planet.pos[0]}|{planet.pos[1]},")
            fileout.write(f"{self.planets[-1].pos[0]}|{self.planets[-1].pos[1]}\n")
        fileout.close()

    def run_animation_from_file(self, filename):
        """
        Reads the data from an already calculated simulation and animates it
        """
        inputdata = []

        # opens transfers all the data that are not commends from the file to the input data list
        filein = open(filename, "r")
        for line in filein.readlines():
            if not line.startswith("#"):
                inputdata.append(line.strip().split(","))
        filein.close()

        # loads the colours and removes them from the data
        colours = inputdata[0]
        inputdata.pop(0)

        # translates the coordinates from string to floats
        for i, line in enumerate(inputdata):
            for j, temp_coord in enumerate(line):
                temp = temp_coord.split("|")
                coordinates = [float(temp[0]), float(temp[1])]
                line[j] = coordinates

        inputdata = inputdata[::5]

        self.patches = []

        max_orb = 6

        # initializes the patches
        for i in range(0, len(inputdata[0])):
            self.patches.append(plt.Circle(inputdata[0][i], max_orb * 0.01, color=colours[i], animated=True))

        # create plot elements
        plt.style.use('dark_background')
        fig = plt.figure()
        ax = plt.axes()

        for i in self.patches:
            ax.add_patch(i)

        # set up the axes
        lim = max_orb
        ax.axis("scaled")
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        plt.ylabel("Y position (AU)")
        plt.xlabel("X position (AU)")

        self.positions_from_file = inputdata

        # create the animator
        anim = FuncAnimation(fig, self.animate_from_file, frames=len(inputdata), repeat=False, interval=30
                             , blit=True)

        # initialization of beeman integration
        self.update_forces()
        for planet in self.planets:
            planet.acc = planet.force / planet.mass
            planet.acc_old = planet.acc

        # saves the animation to file
        anim.save('simulation.gif', writer='pillow', fps=30)

    def animate_from_file(self, i):
        """
        performs one step in the animation that is read from file
        """
        for j, v in enumerate(self.patches):
            v.center = self.positions_from_file[i][j]

        return self.patches
