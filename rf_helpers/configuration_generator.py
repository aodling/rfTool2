import pathlib

import rf_helpers.rf_controller
import example_setups.setup


def generate_ad_file(cfg: example_setups.setup, path: str, controller: rf_helpers.rf_controller, filename: str) -> int:
    print("Doing configuration with signals:")
    for s in cfg.get_signals():
        amp = s.amplitude
        freq = s.frequency
        print("  f={} at {} dBFS".format(freq, amp))

    samples = controller.get_samples(cfg.get_signals())
    print("Creating directory {}".format(path))
    pathlib.Path(path).mkdir(parents = True, exist_ok = True)
    adfile = filename + ".txt"
    try:
        with open(pathlib.Path(path,adfile), 'w') as fp:
            for s in samples:
                fp.write("{:d}\n".format(s))
        with open(pathlib.Path(path,"gen_info.txt"),'w') as fp:
            fp.write("Generated Stimuli file with frequency: {} MHz @ {} dBFS\n".format(controller.get_real_frequency(freq) / 1e6,amp))
            fp.write("The requested frequency was {} MHz, a difference of {} Hz\n".format(freq/1e6,controller.get_real_frequency(freq) - freq))
    except IOError as e:
        print("Couln't create file")
        raise e
    plot = pathlib.Path(path,filename + ".png")
    #Create a spectral plot of the signal as well
    rf_helpers.rf_controller.plot_spectrum(samples, controller, plot)