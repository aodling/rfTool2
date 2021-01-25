from example_setups.generic_configuration import generic_configuration
from example_setups.rfsignal import rfsignal
from example_setups.setup import setup


class temp_small_config(generic_configuration):

    def __init__(self):
        super().__init__()
        frequencies = list([1e6, 1e7])
        for i in range(1, 5):
            frequencies.append(i * 1e8)
        amplitudes = [0, -6]
        for f in frequencies:
            for a in amplitudes:
                s = setup()
                s.add_signal(rfsignal(f,a))
                self.config_list.append(s)

