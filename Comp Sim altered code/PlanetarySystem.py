import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Planet import Planet


class PlanetarySystem:
    """
    represents the solar systems, handles simulation and animation
    """
    def __init__(self, m_vec, pos_mat, vel_mat, limit, step, filename_write="energy.txt", integrator="beeman"):
        m1 = m_vec[0]
        m2 = m_vec[1]
        m3 = m_vec[2]
        pos1 = pos_mat[0]
        pos2 = pos_mat[1]
        vel1 = vel_mat[0]
        vel2 = vel_mat[1]

        # simulation parameters
        self.limit = limit  # the maximum number of iteration
        self.step = step  # the duration of one timestep
        self.g = 1  # the graviational constant

        # list for planets
        self.planets = []

        self.planets.append(Planet(m1, pos1, vel1, name="one", colour="b"))
        self.planets.append(Planet(m2, pos2, vel2, name="two", colour="g"))
        self.planets.append(Planet(m3, -(m1*pos1 + m2*pos2), -(m1*vel1 + m2*vel2), name="three", colour="r"))

        self.energy_history = []  # will store the total energy of the system in each timestep
        self.total_time = 0  # stores the total time
        self.potential_energy = 0  # stores the potential energy

        # selects the appropriate type of integration based on the input
        if integrator == "beeman":
            self.perform_step = getattr(self, "perform_step_beeman")
        elif integrator == "euler":
            self.perform_step = getattr(self, "perform_step_euler")

    def __init__2(self, m_vec, pos1, vel_mat, limit, step, g, filename_write="energy.txt", integrator="beeman"):
        m1 = m_vec[0]
        m2 = m_vec[1]
        pos2 = np.array([1., 0.])
        vel1 = vel_mat[0]
        vel2 = vel_mat[1]

        # simulation parameters
        self.limit = limit  # the maximum number of iteration
        self.step = step  # the duration of one timestep
        self.g = g  # the graviational constant

        # list for planets
        self.planets = []

        self.planets.append(Planet(m1, pos1, vel1, name="one", colour="b"))
        self.planets.append(Planet(m2, pos2, vel2, name="two", colour="g"))
        self.planets.append(Planet(1, -(m1*pos1 + m2*pos2), -(m1*vel1 + m2*vel2), name="three", colour="r"))

        self.energy_history = []  # will store the total energy of the system in each timestep
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
            print(planet.pos)

        # the total energy is stored
        self.energy_history.append(self.get_total_energy())

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
        self.energy_history.append(self.get_total_energy())

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
            self.patches.append(plt.Circle(planet.pos, max_orb * 0.02, color=planet.colour, animated=True))

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
        self.anim = FuncAnimation(fig, self.animate, frames=self.limit, repeat=False, interval=5, blit=True)

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

        self.energy_history.append(self.get_total_energy())

        return self.patches

    def display_energy_graph(self):
        """
        generates a graph of the energy history of the system
        """
        skip = 1
        plt.style.use("default")
        x_values = np.linspace(0, self.total_time, num=len(self.energy_history))
        plt.ylabel("Total energy (joules)")
        plt.xlabel("Time elapsed (earth years)")
        plt.title("Energy vs Time Euler (timestep=0.001)")
        plt.plot(x_values[::skip], self.energy_history[::skip])
        plt.show()

    def print_energy_stats(self):
        """
        prints the average energy of the system and the associated deviation
        """
        mean = sum(self.energy_history) / len(self.energy_history)
        variance = 0
        for energy in self.energy_history:
            variance += (energy - mean)**2

        variance = variance / len(self.energy_history)
        deviation = np.sqrt(variance)
        print(f"The mean energy was {mean} Joules with a standard deviation of {deviation} Joules")

    def get_kinetic_energy(self):
        """
        returns the kinetic energy of the system
        """
        kin_en = 0
        for i in self.planets:
            kin_en += i.get_kinetic_energy()
        return kin_en

    def get_total_energy(self):
        """
        returns the total energy of the system in joules
        """
        # need to convert from earth masses AU^2 yr^-2 to kg m^2 s-2 (J)
        # 1 earth mass = 5.97219e24 kg
        # 1 AU = 1.496e+11 m
        # c = (5.97219e+24 * 1.496e+11 * 1.496e+11) / (3.154e+7 * 3.154e+7)
        # return c * (self.get_kinetic_energy() + self.potential_energy)
        return self.get_kinetic_energy() + self.potential_energy

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

        max_orb = 10

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

