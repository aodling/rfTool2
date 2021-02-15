from example_setups.rfsignal import rfsignal


class setup:

    def __init__(self) -> None:
        self.rfsignals = list()

    def add_signal(self, s: rfsignal):
        self.rfsignals.append(s)

    def get_freqs(self):
        r = list()
        for s in self.get_signals():
            r.append(s.frequency)
        return r

    def get_max_power(self):
        mpow = -100
        for s in self.rfsignals:
            if s.amplitude > mpow:
                mpow = s.amplitude
        return mpow

    def get_signals(self) -> rfsignal:
        return self.rfsignals

    def __str__(self):
        r = "The setup has following signals:\n"
        for s in self.get_signals():
            amp = s.amplitude
            freq = s.frequency
            r += "  f={} at {} dBFS\n".format(freq, amp)
        return r

    def get_filename(self):
        #TODO: Implement something useful
        r = ""
        for s in self.get_signals():
            r += "_F{:04d}_MHz_P{}_dBFS_".format(int(s.frequency/1e6),s.amplitude)
        return r
