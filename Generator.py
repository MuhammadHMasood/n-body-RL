
from Setting import Setting
import numpy as np

class Generator:
    def __init__(self):
        pass

    def generate(self, number, planet_num, type):
        setting = Setting.generate_instance(type, planet_num)
        initial_state, final_state = setting.get_vector_pair(reduction_type=type)
        initial = np.array([initial_state])
        final = np. array([final_state])
        
        for i in range(1, number):
            setting = Setting.generate_instance(type, planet_num)
            initial_state, final_state = setting.get_vector_pair(reduction_type=type)
            initial.append(initial_state)
            final.append(final_state)

        return initial, final
