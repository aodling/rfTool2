from example_setups.generic_configuration import generic_configuration
from example_setups.rfsignal import rfsignal
from example_setups.setup import setup


class single_tone_config_10G(generic_configuration):

    def __init__(self):
        super().__init__()
        super().set_path("singleToneConfigs10G_span")
        super().set_prefix("CW_10Gspan")
        super().set_rbw(100e3)
        super().set_span(10e9)
        frequencies = list([1e6, 1e7])
        for i in range(1, 10):
            frequencies.append(i * 5e8)
        amplitudes = [0, -6]
        for f in frequencies:
            for a in amplitudes:
                s = setup()
                s.add_signal(rfsignal(f, a))
                self.config_list.append(s)

