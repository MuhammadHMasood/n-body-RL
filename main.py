from Setting import Setting
from Planet import Planet
import numpy as np


def main():
    planet1 = Planet(1, np.array([1., 1.]), np.array([0., 1.]))
    planet2 = Planet(1, np.array([-1., -1.]), np.array([0., -1.]))
    setting = Setting(planet1, planet2)

    print("\n", setting)
    # print(setting.simulate_old(), "\n")
    new_setting = setting.reduce(scaled=True)
    new_setting.simulate_old()
    print(setting.reintroduce(new_setting))
    print(new_setting)
    print(setting.reintroduce(new_setting.simulate()))


if __name__=="__main__":
    main()