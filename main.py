# This is a sample Python script.

# Press Skift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import shutil
import subprocess

from example_setups import doble_tone
from time import time, sleep
from example_setups import single_tone_config
from example_setups import single_tone_config_10G
from example_setups.rfsignal import rfsignal
# from example_setups.temp_config import temp_config
# from example_setups.temp_small_config import temp_small_config
from rf_helpers.rf_controller import rfController
from rf_helpers import configuration_generator
from common_math.math import safe_log10
from pathlib import Path

do_plots = True
try:
    import matplotlib.pyplot as plt
    import numpy as np
except ModuleNotFoundError:
    do_plots = False
    print("Ignoring plots")

use_spec = True
try:
    from rs_integration.rs_integration import instrument_init, clear_specan, do_basic_sweep, disconnect, \
        store_config_string
except ModuleNotFoundError as e:

    use_spec = False
    raise e


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def get_configurations():
    pass


def get_adc_string(y_in):
    ret = ""
    for v in y_in:
        ret += "{:d}\n".format(v)
    return ret


def download_cfg(d, filename: str):
    cmd = ["scp", "-i", "C:\\MinGW\\msys\\1.0\\home\\TRx\\.ssh\\id_rsa", Path(d) / filename,
           "root@192.168.0.10:datat.txt"]
    print(cmd)
    # print(" ".join(cmd))
    print("Downloading config {}".format(d))
    r = subprocess.run(cmd, timeout=100, text=True, capture_output=True)
    print("Download Completed. Loading vector...")
    cmdrun = ["ssh", "-i", "C:\\MinGW\\msys\\1.0\\home\\TRx\\.ssh\\id_rsa", "root@192.168.0.10",
              "./ad9083_xtra/app_ads9/debug/ad9081_xtra tx --file datat.txt"]
    r = subprocess.run(cmdrun, timeout=1000, text=True, capture_output=True)
    print("Downloaded vector.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    specan = None
    p = rfController(12e9)

    y = p.get_samples([rfsignal(5e9, -12)])
    x = p.get_xaxis()
    if do_plots:
        fig, axs = plt.subplots(3, 1, constrained_layout=True)

        axs[0].plot(x, y)
        axs[0].set_title("Time plot")
        axs[0].set_xlabel("Time (s)")
        axs[0].set_ylabel("ADC Value")

        Y = np.fft.fft(y / p.get_max_mag())
        # Windowing function
        win = np.ones(len(Y), dtype=int)
        # Magnitude spectrum with compensation for real spectrum  and windowing
        s_mag = np.abs(Y) * 2 / np.sum(win)
        s_dbfs = 20 * safe_log10(s_mag)
        freq = np.fft.fftfreq(len(Y), d=p.Ts)

        axs[1].plot(freq, s_dbfs)
        axs[1].set_title("Spectral Plot")
        axs[1].set_xlabel("Frequency (Hz)")
        axs[1].set_ylabel("Power (dBFS)")
        axs[1].axis([np.min(freq), np.max(freq), -100, 0])
        axs[1].grid(True)

        Y = np.fft.fft(np.concatenate((y, y)) / p.get_max_mag())
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

        # plt.show()

    # print(get_adc_string(y))
    # This should be like this
    # stc = temp_config()
    # But now it is
    startTime = time()
    dc = single_tone_config.default_config()
    stc = single_tone_config.single_tone_config()
    ttc = doble_tone.two_tone_config()
    tenc = single_tone_config_10G.single_tone_config_10G()
    path = "tmpout"
    filename = "testfile1.txt"
    configuration_generator.generate_ad_file(stc.config_list[0], path, p, filename)
    i = 0

    confs_to_run = [dc,ttc, tenc, stc ]
    # confs_to_run = [dc, ttc]
    # confs_to_run = [dc]
    # confs_to_run = [dc, tenc, stc]
    cvs_hdr = "freq,pwr,fmeas0,pwr0,fmeas1,pwr1,fmeas2,pwr2,fmeas3,pwr3,fmeas4,pwr4,fmeas5,pwr5"

    for c in confs_to_run:
        c.get_cfg_length()
    sleep(5)
    if use_spec:
        specan = instrument_init("10.10.0.231")
        print("Clearing data on SPECAN")
        clear_specan(specan, True)
        # Clear all previous data
    for config in confs_to_run:
        i = 0
        try:
            shutil.rmtree(config.get_path())
        except FileNotFoundError:
            pass
        #Write CVS File
        cvs_filename = Path(config.get_path()) / "maxpoints.cvs"
        cvs_filename_narrow = Path(config.get_path()) / "maxpoints_narrow.cvs"
        Path(config.get_path()).mkdir(parents=True,exist_ok=True)
        with open(cvs_filename,'w') as fp:
            fp.write(cvs_hdr + "\n")
        with open(cvs_filename_narrow, 'w') as fp:
                fp.write(cvs_hdr + "\n")

        for cfg in config:
            path = "{}/{}".format(config.get_path(), "gen_data")  # config.get_filename(i))
            filename = config.get_filename(i)
            configuration_generator.generate_ad_file(cfg, path, p, filename)
            i += 1
            # Configure Spec
            if use_spec:
                # DOn't download if no spec is configured
                download_cfg(path, filename + ".txt")
                if cfg.get_max_power() > -20:
                    reflev = 0
                else:
                    reflev = -20
                f = cfg.get_freqs()
                freal = p.get_real_frequency(f[0])
                print(freal)
                maxList = do_basic_sweep(specan, output_folder=config.get_path(), span_MHz=config.get_span_MHz(),
                                         filename=filename,
                                         rbw_khz=config.get_rbw_kHz(), rlev=reflev)#, M1freq=freal)
                # Do a zoomed Sweep. If only one freq, center around that freq. Else: CF = mean(freq)
                # span = f[1] - f[0]
                span = 2;
                cf = freal;
                if len(f) > 1:
                    span = 1.1 * (f[1]-f[0])
                    span /= 1e6
                    cf   = (f[1] + f[0]) / 2

                maxListZoomed = do_basic_sweep(specan, output_folder=config.get_path(), span_MHz=span,
                                               center_freq=cf,
                                         filename="2_MHzSpan_" + filename,
                                         rbw_khz=0.1, rlev=reflev)#, M1freq=freal)
                mp = cfg.get_max_power()
                f = cfg.get_freqs()
                freal = p.get_real_frequency(f[0])
                # print(maxList)
                cvsstr = "{},{}".format(freal,mp)
                for e in maxList:
                    cvsstr += ",{},{}".format(e[0],e[1])
                cvsstr += "\n"
                with open(cvs_filename,'a') as fp:
                    fp.write(cvsstr)
                # Do it again for narrow config
                cvsstr = "{},{}".format(freal, mp)
                for e in maxListZoomed:
                    cvsstr += ",{},{}".format(e[0], e[1])
                cvsstr += "\n"
                with open(cvs_filename_narrow, 'a') as fp:
                    fp.write(cvsstr)
                store_config_string(specan, output_folder=config.get_path(), filename=filename)
    if use_spec:
        disconnect(specan)
    stopTime = time()
    print(f'Total Runtime: {stopTime - startTime:.3f} secs')

    # Get Data From Spec to Path
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
