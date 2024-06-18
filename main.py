from Setting import Setting
from Planet import Planet
import numpy as np


def main():
    """""
    # planet1 = Planet(1, np.array([1., 1.]), np.array([0., 1.]))
    # planet2 = Planet(1, np.array([-1., -1.]), np.array([0., -1.]))

    print("\n", setting)
    print(setting.simulate_old(), "\n")
    new_setting = setting.reduce(centered=True, scaled=True, g_removed=True, step_removed=True)   
    
    # print(new_setting)
    # print(setting.reintroduce(new_setting), "\n")
    a = new_setting.simulate_old()
    print(a)
    print(setting.reintroduce(a), "\n")
    """""
    setting = Setting.generate_instance("none", 3)
    #planet1 = Planet(1, np.array([1., 1.]), np.array([1., 0.]))
    #planet2 = Planet(1, np.array([-1., 1.]), np.array([-1., 0.]))
    #setting = Setting(planet1, planet2, step=2)
    print(setting.simulate(), "\n")
    print(setting.simulate_old(), "\n")
    new_setting = setting.reduce(centered=True, scaled=True, g_removed=True, step_removed=True)
    # print(new_setting, "\n")
    # a = new_setting.simulate_old()
    # print(a)
    # print(setting.reintroduce(a), "\n")
    a = new_setting.simulate()
    # print(a)
    print(setting.reintroduce(a), "\n")




if __name__=="__main__":
    main()