from math import sin, pi
import numpy as np

class rfController:

    def __init__(self, Fs, length= 2**14, resolution= 2**12):
        self.Fs = int(Fs)
        self.length = length
        self.resolution = int(resolution/2)
        self.Ts = 1/self.Fs

    def _tot_time(self):
        return self.Ts * self.length

    def get_max_mag(self):
        return self.resolution

    def get_samples(self, frequency, dBFS):
        A = self.resolution * 10 ** (dBFS / 20)
        T = 1 / frequency
        Treal = round(self._tot_time() / T) / self._tot_time()

        freq = Treal
        y = np.zeros(self.length,np.int32)

        for i in range(0, self.length):
            y[i] = int(A*sin(2*pi*freq*i*self.Ts))
        return y

    def get_xaxis(self):
        ret = np.arange(self.length, dtype=float)
        ret *= self.Ts
        return ret
