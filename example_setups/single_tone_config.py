from example_setups.generic_configuration import generic_configuration
from example_setups.setup import setup


class single_tone_config(generic_configuration):

    def __init__(self):
        super().__init__()
        frequencies = list([1e6, 1e7])
        for i in range(1, 50):
            frequencies.append(i * 1e8)
        amplitudes = [0, -3, -6, -20]
        for f in frequencies:
            for a in amplitudes:
                self.config_list.append(setup(f,a))

