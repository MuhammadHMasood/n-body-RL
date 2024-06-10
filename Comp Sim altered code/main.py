from PlanetarySystem import PlanetarySystem
import numpy as np


def main():
    m_vec = np.array([1, 1, 1])
    pos_mat = np.array([[0.5, np.sqrt(2)/2],
                        [0.5, -np.sqrt(2)/2]])
    vel_mat = np.array([[1., 0.],
                        [0., 1.]])
    system = PlanetarySystem(m_vec, pos_mat, vel_mat, 10000, 0.01, 1, integrator="beeman")
    system.run_animation()


if __name__ == "__main__":
    main()
