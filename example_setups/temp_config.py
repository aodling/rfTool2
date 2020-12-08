from example_setups.generic_configuration import generic_configuration
from example_setups.rfsignal import rfsignal
from example_setups.setup import setup


class temp_config(generic_configuration):

    def __init__(self):
        super().__init__()
        super().set_path("tmpCfg")
        frequencies = list([1e8])
        for i in range(7, 10):
            frequencies.append(i * 1e8)
        amplitudes = [0, -6]
        for f in frequencies:
            for a in amplitudes:
                s = setup()
                s.add_signal(rfsignal(f,a))
                s.add_signal(rfsignal(1111e6,-12))
                self.config_list.append(s)

