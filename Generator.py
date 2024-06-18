
from Setting import Setting
import numpy as np
import time

class Generator:
    def __init__(self):
        pass

    def generate(self, number, planet_num, type):
        setting = Setting.generate_instance(type, planet_num)
        initial_state, final_state = setting.get_vector_pair(reduction_type=type)
        initial = np.array([initial_state])
        final = np. array([final_state])

        for _ in range(1, number):
            setting = Setting.generate_instance(type, planet_num)
            initial_state, final_state = setting.get_vector_pair(reduction_type=type)
            initial = np.row_stack((initial, initial_state))
            final = np.row_stack((final, final_state))

        return initial, final

generator = Generator()

start = time.time()

a, b = generator.generate(1000, 3, "full")

end = time.time()

print(a, "\n")
print(b)
print(end - start)