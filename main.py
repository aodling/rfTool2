# This is a sample Python script.

# Press Skift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import shutil
import subprocess

import matplotlib.pyplot as plt
import numpy as np

from example_setups import single_tone_config
from example_setups.rfsignal import rfsignal
from example_setups.temp_config import temp_config
from example_setups.temp_small_config import temp_small_config
from rf_helpers.rf_controller import rfController
from rf_helpers import configuration_generator
from common_math.math import safe_log10
from pathlib import Path

from rs_integration.rs_integration import instrument_init, clear_specan, do_basic_sweep, disconnect


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



def get_configurations():
    pass


def get_adc_string(y):
    ret =""
    for v in y:
        ret += "{:d}\n".format(v)
    return ret

def download_cfg(d,filename : str):
    cmd = ["scp","-i", "C:\\MinGW\\msys\\1.0\\home\\TRx\\.ssh\\id_rsa", Path(d) / filename, "root@192.168.0.10:datat.txt"]
    print(cmd)
    #print(" ".join(cmd))
    print("Downloading config {}".format(d))
    subprocess.run(cmd, timeout=100)
    print("Download Completed. Loading vector...")
    cmdrun = ["ssh","-i", "C:\\MinGW\\msys\\1.0\\home\\TRx\\.ssh\\id_rsa", "root@192.168.0.10",
              "./ad9083_xtra/app_ads9/debug/ad9081_xtra tx --file datat.txt"]
    subprocess.run(cmdrun,timeout = 1000)
    print("Downloaded vector.")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    p = rfController(12e9)

    y = p.get_samples([rfsignal(5e9,-12)])
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


    #plt.show()

    #print(get_adc_string(y))
    # This should be like this
    #stc = temp_config()
    # But now it is
    stc = single_tone_config.default_config()
    path = "tmpout"
    filename = "testfile1.txt"
    configuration_generator.generate_ad_file(stc.config_list[0], path, p, filename)
    i = 0

    specan = instrument_init("10.10.0.231")
    print("Clearing data on SPECAN")
    clear_specan(specan,True)
    #Clear all previous data
    try:
        shutil.rmtree("stc")
    except FileNotFoundError:
        pass
    for cfg in stc:
        path = "{}/cfg{}".format(stc.get_path(),i)
        filename = stc.get_filename(i)
        configuration_generator.generate_ad_file(cfg, path, p, filename)
        i += 1
        download_cfg(path, filename + ".txt")

        # Configure Spec
        do_basic_sweep(specan,output_folder=path)

        #Get Data From Spec to Path

    disconnect(specan)
    #print(stc.print_configuration())

