# Example for FSW / FSV / FSVA / FPS Spectrum Analyzers
# Preconditions:
# - Installed RsInstrument Python module Version 1.8.0 or newer from pypi.org
# - Installed VISA e.g. R&S Visa 5.12.x or newer
from pathlib import Path

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
from time import time, sleep
import os


def instrument_init(ipaddr: str):
    specan = None
    try:
        # Adjust the VISA Resource string to fit your instrument
        specan = RsInstrument('TCPIP::{}::INSTR'.format(ipaddr), True, False)
        specan.assert_minimum_version('1.8.0')
        specan.visa_timeout = 3000  # Timeout for VISA Read Operations
        specan.opc_timeout = 3000  # Timeout for opc-synchronised operations
        specan.instrument_status_checking = True  # Error check after each command
    except Exception as ex:
        print('Error initializing the instrument session:\n' + ex.args[0])
        exit()
    print(f'Driver Version: {specan.driver_version}')
    print(f'SpecAn IDN: {specan.idn_string}')
    print(f'SpecAn Options: {",".join(specan.instrument_options)}')
    return specan


def clear_specan(specan, UpdateDisplay: bool = False):
    if UpdateDisplay:
        onoff = "ON"
    else:
        onoff = "OFF"
    specan.clear_status()
    specan.reset()
    specan.write_str('INIT:CONT OFF')  # Switch OFF the continuous sweep
    specan.write_str('SYST:DISP:UPD ' + onoff)  # Display update ON - switch OFF after debugging


# -----------------------------------------------------------
# Basic Settings:
# -----------------------------------------------------------

def do_basic_sweep(specan, center_freq : float = 3 , span_MHz : float = 200,
                   rlev = 0.0,
                   rbw_khz = 100,
                   output_folder = r"C:\Temp\\" ,
                   filename = "measured"):
    specan.write_str('DISP:WIND:TRAC:Y:RLEV {:.1f}'.format(rlev))  # Setting the Reference Level
    specan.write_str('FREQ:CENT {:.1f} GHz'.format(center_freq))  # Setting the center frequency
    specan.write_str('FREQ:SPAN {:.1f} MHz'.format(span_MHz))  # Setting the span
    specan.write_str('BAND {} kHz'.format(int(rbw_khz)))  # Setting the RBW
    specan.write_str('BAND:VID {} kHz'.format(int(rbw_khz)))  # Setting the VBW
    specan.write_str('SWE:POIN 65536')  # Setting the sweep points
    specan.query_opc()  # Using *OPC? query waits until all the instrument settings are finished
    # -----------------------------------------------------------
    # SyncPoint 'SettingsApplied' - all the settings were applied
    # -----------------------------------------------------------
    specan.VisaTimeout = 2000  # Sweep timeout - set it higher than the instrument acquisition time
    specan.write_str_with_opc('INIT')  # Start the sweep and wait for it to finish
    # -----------------------------------------------------------
    # SyncPoint 'AcquisitionFinished' - the results are ready
    # -----------------------------------------------------------
    # Fetching the trace
    # The functions are universal for binary or ascii data format
    # -----------------------------------------------------------
    t = time()
    trace = specan.query_bin_or_ascii_float_list('FORM ASC;:TRAC? TRACE1')  # Query ascii array of floats
    print(f'Instrument returned {len(trace)} points in the ascii trace, query duration {time() - t:.3f} secs')

    if not os.path.exists(Path(output_folder) / "data_trace"):
        os.makedirs(Path(output_folder) / "data_trace")
        os.makedirs(Path(output_folder) / "bintrace")
        os.makedirs(Path(output_folder) / "SA_screendump")
        os.makedirs(Path(output_folder) / "sa_config")


    with open(Path(output_folder) / "data_trace" / "{}.trace".format(filename),'w') as fp:
        for e in trace:
            fp.write(str(e) + "\n")
    t = time()
    specan.bin_float_numbers_format = BinFloatFormat.Single_4bytes  # This tells the driver in which format to expect the binary float data
    trace = specan.query_bin_or_ascii_float_list(
        'FORM REAL,32;:TRAC? TRACE1')  # Query binary array of floats - the query function is the same as for the ASCII format



    with open(Path(output_folder) / "bintrace" / "{}.bintrace".format(filename),'w') as fp:
        for e in trace:
            fp.write(str(e) + "\n")
    print(f'Instrument returned {len(trace)} points in the binary trace, query duration {time() - t:.3f} secs')
    # -----------------------------------------------------------
    # Setting the marker to max and querying the X and Y
    # -----------------------------------------------------------
    for m in range (1,6):
        specan.write_str_with_opc(
            'CALC1:MARK{}:MAX'.format(int(m)))  # Set the marker to the maximum point of the entire trace, wait for it to be set
        for n in range(1,m):
            specan.write_str_with_opc('CALC1:MARK{}:MAX:NEXT'.format(int(m)))
    # specan.write_str_with_opc('CALC1:MARK3:MAX:NEXT')
    # specan.write_str_with_opc('CALC1:MARK4:MAX:NEXT')
    # specan.write_str_with_opc('CALC1:MARK5:MAX:NEXT')
    #CALCulate<1|2>:DELTamarker<1...4>:MAXimum:NEXT
    markerX = specan.query_float('CALC1:MARK1:X?')
    markerY = specan.query_float('CALC1:MARK1:Y?')
    maxList =list()
    maxList.append([markerX,markerY])
    print(f'Marker Frequency {markerX:.2f} Hz, Level {markerY:.3f} dBm')
    for i in range(2,6):
        markerX = specan.query_float('CALC1:MARK{}:X?'.format(int(i)))
        markerY = specan.query_float('CALC1:MARK{}:Y?'.format(int(i)))
        maxList.append([markerX, markerY])


    # -----------------------------------------------------------
    # Making an instrument screenshot and transferring the file to the PC
    # -----------------------------------------------------------
    specan.write_str("HCOP:DEV:LANG PNG")
    specan.write_str(r"MMEM:NAME 'c:\temp\Dev_Screenshot.png'")
    specan.write_str("HCOP:IMM")  # Make the screenshot now
    specan.query_opc()  # Wait for the screenshot to be saved
    p = Path(output_folder) / "SA_screendump" / "{}.png".format(filename)
    specan.read_file_from_instrument_to_pc(r"c:\temp\Dev_Screenshot.png",
                                           str(p.absolute()))  # Transfer the instrument file to the PC
    print("Instrument screenshot file saved to PC '{}'".format(p.absolute()))
    return  maxList
def store_config_string(specan,
                   output_folder = r"C:\Temp\\" ,
                   filename = "measured"):
    rbw = specan.query_float("BAND?")
    ref_lvl = specan.query_float('DISP:WIND:TRAC:Y:RLEV?')  # Setting the Reference Level
    cf =  specan.query_float("FREQ:CENT?")
    span = specan.query_float('FREQ:SPAN?')
    att = specan.query_float('INP:ATT?')
    s = ""
    s += "RBW,{}\n".format(rbw)
    s += "RefLvl,{}\n".format(ref_lvl)
    s += "CenterFreq,{}\n".format(cf)
    s += "Span,{}\n".format(span)
    s += "Att,{}\n".format(att)

    p = Path(output_folder) / "sa_config" / "{}.txt".format(filename)
    with open(p,'w') as fp:
        fp.write(s)



# Close the session
def disconnect(specan):
    specan.close()
