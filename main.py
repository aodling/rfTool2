# This is a sample Python script.

# Press Skift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import shutil
import subprocess
from  example_setups import doble_tone
from time import time
do_plots =  True
try:
    import matplotlib.pyplot as plt
    import numpy as np
except ModuleNotFoundError:
    do_plots = False
    print("Ignoring plots")

from example_setups import single_tone_config
from example_setups import single_tone_config_10G
from example_setups.rfsignal import rfsignal
from example_setups.temp_config import temp_config
from example_setups.temp_small_config import temp_small_config
from rf_helpers.rf_controller import rfController
from rf_helpers import configuration_generator
from common_math.math import safe_log10
from pathlib import Path
use_spec = True
try:
    from rs_integration.rs_integration import instrument_init, clear_specan, do_basic_sweep, disconnect, store_config_string
except ModuleNotFoundError as e:
    raise e
    use_spec = False


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
    if do_plots:
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
    startTime = time()
    dc  = single_tone_config.default_config()
    stc = single_tone_config.single_tone_config()
    ttc = doble_tone.two_tone_config()
    tenc = single_tone_config_10G.single_tone_config_10G()
    path = "tmpout"
    filename = "testfile1.txt"
    configuration_generator.generate_ad_file(stc.config_list[0], path, p, filename)
    i = 0
    confs_to_run = [dc]
    confs_to_run = [dc, tenc, stc, ttc]
    if use_spec:
        specan = instrument_init("10.10.0.231")
        print("Clearing data on SPECAN")
        clear_specan(specan,True)
        #Clear all previous data
    for config in confs_to_run:
        i = 0
        try:
            shutil.rmtree(config.get_path())
        except FileNotFoundError:
            pass
        for cfg in config:
            path = "{}/{}".format(config.get_path(),config.get_filename(i))
            filename = config.get_filename(i)
            configuration_generator.generate_ad_file(cfg, path, p, filename)
            i += 1
            # Configure Spec
            if use_spec:
                #DOn't download if no spec is configured
                download_cfg(path, filename + ".txt")
                do_basic_sweep(specan,output_folder=path,span_MHz=config.get_span_MHz(),filename = filename,
                               rbw_khz=config.get_rbw_kHz())
                store_config_string(specan,output_folder=path,filename=filename)
    if use_spec:
        disconnect(specan)
    stopTime = time()
    print(f'Total Runtime: {stopTime - startTime:.3f} secs')

            #Get Data From Spec to Path
"""    i = 0
    path = ttc.get_path()
    try:
        shutil.rmtree(ttc.get_path())
    except FileNotFoundError:
        pass
    for cfg in ttc:
        path = "{}/cfg{}".format(ttc.get_path(), i)
        filename = ttc.get_filename(i)
        configuration_generator.generate_ad_file(cfg, path, p, filename)
        i += 1
"""



