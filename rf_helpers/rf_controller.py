from math import sin, pi
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from common_math.math import safe_log10
from example_setups.setup import setup


class rfController:

    def __init__(self, Fs, length=2 ** 14, resolution=2 ** 16):
        self.Fs = int(Fs)
        self.length = length
        self.resolution = int((resolution-1) / 2)
        self.Ts = 1 / self.Fs

    def _tot_time(self):
        return self.Ts * self.length

    def get_max_mag(self):
        return self.resolution

    def get_samples(self, stup: list):
        y = np.zeros(self.length, np.int32)
        for s in stup:
            dBFS = s.amplitude
            frequency = s.frequency
            A = self.resolution * 10 ** (dBFS / 20)
            freq = self.get_real_frequency(frequency)
            for i in range(0, self.length):
                y[i] += int(round(A * sin(2 * pi * freq * i * self.Ts)))
                if y[i] > self.get_max_mag():
                    y[i] = self.get_max_mag()
                elif y[i] < - self.get_max_mag():
                    y[i] = 0 - self.get_max_mag()
        return y

    def get_real_frequency(self, frequency) -> float:
        if frequency == 0:
            return 0.0
        T = 1 / frequency
        Treal = round(self._tot_time() / T) / self._tot_time()
        freq = Treal
        return freq

    def get_xaxis(self):
        ret = np.arange(self.length, dtype=float)
        ret *= self.Ts
        return ret


def plot_spectrum(y: list, p: rfController, fn: Path = None):
    fig, axs = plt.subplots(1, 1, constrained_layout=True)
    Y = np.fft.fft(y / p.get_max_mag())
    # Windowing function
    win = np.ones(len(Y), dtype=int)
    # Magnitude spectrum with compensation for real spectrum  and windowing
    s_mag = np.abs(Y) * 2 / np.sum(win)
    s_dbfs = 20 * safe_log10(s_mag)
    freq = np.fft.fftfreq(len(Y), d=p.Ts)

    axs.plot(freq, s_dbfs)
    axs.set_title("Spectral Plot")
    axs.set_xlabel("Frequency (Hz)")
    axs.set_ylabel("Power (dBFS)")
    axs.axis([np.min(freq), np.max(freq), -100, 0])
    axs.grid(True)

    if fn != None:
        plt.savefig(fn)
    plt.close(fig)
