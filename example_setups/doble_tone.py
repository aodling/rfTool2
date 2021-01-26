from example_setups.generic_configuration import generic_configuration
from example_setups.rfsignal import rfsignal
from example_setups.setup import setup


class two_tone_config(generic_configuration):

    def __init__(self):
        super().__init__()
        super().set_path("two_tone_cfg")
        super().set_prefix("2TONE")
        super().set_rbw(100e3)
        frequencies = list()
        for i in range(1, 100):
            frequencies.append(i * 5e7)
        amplitudes = [0, -3, -6, -20]
        separation = [1e6, 1e7, 1e8]
        for a in amplitudes:
            for f in frequencies:
                for sep in separation:
                    s = setup()
                    #Add signal - and + separation
                    s.add_signal(rfsignal(f - sep/2, a))
                    s.add_signal(rfsignal(f + sep / 2, a))
                    self.config_list.append(s)



class default_config(generic_configuration):
    def __init__(self):
        super().__init__()
        super().set_path("defaultConfig")
        frequencies = list([35e8,36e8])
        amplitudes = [-3]
        for f in frequencies:
            for a in amplitudes:
                s = setup()
                s.add_signal(rfsignal(f, a))
                self.config_list.append(s)

class default_config(generic_configuration):
    def __init__(self):
        super().__init__()
        super().set_path("defaultConfig")
        frequencies = list([35e8,36e8])
        amplitudes = [0, -3, -6, -20]
        for f in frequencies:
            for a in amplitudes:
                s = setup()
                s.add_signal(rfsignal(f, a))
                self.config_list.append(s)
