import argparse
import time
import brainflow
import numpy as np
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations


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
    while(time.time()-init<300):
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
        print("theta/alpha:%f", band_power_theta / band_power_alpha)
    board.stop_stream()
    """
    board.release_session()

    eeg_channels = board_descr['eeg_channels']
    # second eeg channel of synthetic board is a sine wave at 10Hz, should see huge alpha
    eeg_channel = eeg_channels[1]
    # optional detrend
    DataFilter.detrend(data[eeg_channel], DetrendOperations.LINEAR.value)
    psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate,
                                WindowFunctions.BLACKMAN_HARRIS.value)

    band_power_alpha = DataFilter.get_band_power(psd, 8.0, 13.0)
    band_power_theta = DataFilter.get_band_power(psd, 4.0, 8.0)
    print("theta/alpha:%f", band_power_theta / band_power_alpha)
    sendtogui = {
    "theta": band_power_theta,
    "alpha": band_power_alpha,

    }
    """


   # return sendtogui
run()

