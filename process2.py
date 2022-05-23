from turtle import bgcolor

import tkinter
from tkinter import *
from tkinter import Button, GROOVE
from threading import *
import time
import simpleaudio as sa
starttime = time.time()
import argparse
import brainflow
import numpy as np

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations


clicked = False
bench = 0
initialratio = 0
def run():
    
  
    BoardShim.enable_dev_board_logger()
    """
    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=True, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=True, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=True)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    args = parser.parse_args()
    """

    params = BrainFlowInputParams()
    params.ip_port = 0
    params.serial_port = 'COM3'
    params.mac_address = 'c7:86:fd:64:9c:e0'
    params.other_info = ""
    params.serial_number = ""
    params.ip_address = ""
    params.ip_protocol = 0
    params.timeout = 0


    board = BoardShim(1, params)
    board_descr = BoardShim.get_board_descr(1)
    #print(board_descr)
    master_board_id = 1
    sampling_rate = BoardShim.get_sampling_rate(master_board_id)
    board.prepare_session()

    # use synthetic board for demo
    """
    params = BrainFlowInputParams()
    board_id = BoardIds.SYNTHETIC_BOARD.value
    
    sampling_rate = int(board_descr['sampling_rate'])
    board = BoardShim(board_id, params)
    board.prepare_session()
    """
    board.start_stream()
    init = time.time()
    while time.time()-init<300 and clicked == False:
        BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
        time.sleep(5)
        nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
        print(nfft)
        data = board.get_current_board_data(sampling_rate*(int(round(time.time()-init))))
        eeg_channels = board_descr['eeg_channels']
        eeg_channel = eeg_channels[1]
        DataFilter.detrend(data[eeg_channel], DetrendOperations.LINEAR.value)
        psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate,
                                    WindowFunctions.BLACKMAN_HARRIS.value)

        band_power_alpha = DataFilter.get_band_power(psd, 8.0, 13.0)
        band_power_theta = DataFilter.get_band_power(psd, 4.0, 8.0)
        information.insert("end", get_timestamp() + ": Data Received\n")
        information.insert("end", "Alpha band power: " + str(round(band_power_alpha,2))+ "\n")
        information.insert("end", "Theta band power: " + str(round(band_power_theta,2))+"\n")
        information.insert("end", "Alpha/Theta Ratio: " + str(round(band_power_alpha/band_power_theta, 2)) + "\n")
        print("theta/alpha:%f", band_power_theta / band_power_alpha)
        if(band_power_theta/band_power_alpha >1/(0.4)):
            information.insert("end", "SLEEP DETECTED, ISSUING ALERT\n")  
            status['bg'] = '#c93a44'
            wave_obj = sa.WaveObject.from_wave_file("ding.wav")
            play_obj = wave_obj.play()
            play_obj.wait_done()
        else:
            status['bg'] = "#57ab6d"

        
            
    information.insert("end", get_timestamp()+ ": Exiting session\n")
    information.see("end")   
    board.stop_stream()

def click():
    global clicked
    clicked = True
    
def get_timestamp():
    return str(round(time.time()-starttime, 2))

def threading():
    # Call work function
    information.insert("end", get_timestamp() + ": Starting Data Collection\n")
    t1=Thread(target=run)
    t1.start()
    

        
theme = {
    "main": 8,
    "title": 17,
    "labelcol": '#ffe8f0'

}

root = Tk()
root.configure(background='pink')
root.geometry("350x375") 
label = Label(root, text = "EEG Sleep Diagnosis", font = ("Arial", theme["title"]), bg = theme["labelcol"])
instructions = Label(root, text="Insert bluetooth dongle into computer, \nmake sure EEG is on, and press start collection", bg = theme["labelcol"])
status = Frame(root, bg = "#57ab6d", height = 30, width = 200)
information = Text(root, borderwidth= 2, relief = GROOVE, width = 40, height = 7, bg = theme["labelcol"])

start = Button(root, text="START COLLECTION", command = threading, relief = GROOVE, width = 17, height = 3, font = ("Arial", theme["main"]), bg = theme["labelcol"])
end = Button(root, text = "STOP COLLECTION", command = click, relief = GROOVE, width = 17, height = 3, font = ("Arial", theme["main"]), bg = theme["labelcol"])
label.pack(padx = 15, pady = 10)

instructions.pack(pady = 5)
status.pack(pady = 10)
information.pack(pady = 5)
start.pack(padx = 30, side = LEFT)
end.pack(padx = 30, side = RIGHT)



root.mainloop()



