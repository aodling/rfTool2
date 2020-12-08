from example_setups.rfsignal import rfsignal


class setup:

    def __init__(self) -> None:
        self.rfsignals = list()

    def add_signal(self, s: rfsignal):
        self.rfsignals.append(s)

    def get_signals(self) -> rfsignal:
        return self.rfsignals

    def __str__(self):
        r = "The setup has following signals:\n"
        for s in cfg.get_signals():
            amp = s.amplitude
            freq = s.frequency
            r += "  f={} at {} dBFS\n".format(freq, amp)
        return r

