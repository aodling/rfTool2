# This is a sample Python script.

# Press Skift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import matplotlib.pyplot as plt
import numpy as np
from rfController import rfController

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def safe_log10(x, eps=1e-10):
    result = np.where(x > eps, x, -10)
    np.log10(result, out=result, where=result > 0)
    return result


frequencies = [1e9, 2e9, 3e9, 4e9, 5e9]
amplitudes  = [0, -3, -6, -12]



def get_configurations():
    pass
    

def get_adc_string(y):
    ret =""
    for v in y:
        ret += "{:d}\n".format(v)
    return ret

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    p = rfController(12e9)

    y = p.get_samples(5e9,-12)
    x = p.get_xaxis()

    fig, axs = plt.subplots(3, 1, constrained_layout=True)

    axs[0].plot(x,y)
    axs[0].set_title("Time plot")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("ADC Value")

    Y = np.fft.fft(y/p.get_max_mag())
    #Windowing function
    win = np.ones( len(Y),dtype = int)
    #Magnitude spectrum with compensation for real spectrum  and windowing
    s_mag = np.abs(Y) * 2 / np.sum(win)
    s_dbfs = 20 * safe_log10(s_mag)
    freq = np.fft.fftfreq(len(Y), d=p.Ts)

    axs[1].plot(freq, s_dbfs)
    axs[1].set_title("Spectral Plot")
    axs[1].set_xlabel("Frequency (Hz)")
    axs[1].set_ylabel("Power (dBFS)")
    axs[1].axis([np.min(freq), np.max(freq), -100,0])
    axs[1].grid(True)

    Y = np.fft.fft(np.concatenate((y,y)) / p.get_max_mag())
    # Windowing function
    win = np.ones(len(Y), dtype=int)
    # Magnitude spectrum with compensation for real spectrum  and windowing
    s_mag = np.abs(Y) * 2 / np.sum(win)
    s_dbfs = 20 * safe_log10(s_mag)
    freq = np.fft.fftfreq(len(Y), d=p.Ts)

    axs[2].plot(freq, s_dbfs)
    axs[2].set_title("Spectral Plot")
    axs[2].set_xlabel("Frequency (Hz)")
    axs[2].set_ylabel("Power (dBFS)")
    axs[2].axis([np.min(freq), np.max(freq), -100, 0])
    axs[2].grid(True)


    plt.show()

    print(get_adc_string(y))

