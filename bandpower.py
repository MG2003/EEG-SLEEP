import argparse
import time
import brainflow
import numpy as np

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations


def run():
    
  
    BoardShim.enable_dev_board_logger()

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=15)

    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
 
    parser.add_argument('--board-id', type=int, required = False, help='board id, check docs to get a list of supported boards')

    args = parser.parse_args()
    params = BrainFlowInputParams()
    params.serial_port = 'dongle serial port(COM3, /dev/ttyUSB0…)'
    params.mac_address = 'c7:86:fd:64:9c:e0'
    params.timeout = '15'

    board = BoardShim(1, params)
    master_board_id = 1
    board_descr = BoardShim.get_board_descr(args.board_id)
    sampling_rate = BoardShim.get_sampling_rate(master_board_id)
    board.prepare_session()
    # use synthetic board for demo
    """
    params = BrainFlowInputParams()
    board_id = BoardIds.SYNTHETIC_BOARD.value
    board_descr = BoardShim.get_board_descr(board_id)
    sampling_rate = int(board_descr['sampling_rate'])
    board = BoardShim(board_id, params)
    board.prepare_session()
    """
    board.start_stream()

 
     
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(5)
    nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
    print(nfft)
    data = board.get_board_data()

    board.stop_stream()
    board.release_session()

    eeg_channels = board_descr['eeg_channels']
    # second eeg channel of synthetic board is a sine wave at 10Hz, should see huge alpha
    eeg_channel = eeg_channels[0]
    # optional detrend
    DataFilter.detrend(data[eeg_channel], DetrendOperations.LINEAR.value)
    psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate,
                                WindowFunctions.BLACKMAN_HARRIS.value)

    band_power_alpha = DataFilter.get_band_power(psd, 7.0, 13.0)
    band_power_theta = DataFilter.get_band_power(psd, 4.0, 7.0)
    print("theta/alpha:%f", band_power_theta / band_power_alpha)
  

    # fail test if ratio is not smth we expect

    if (band_power_theta / band_power_alpha < 100):
        return 0
    else:
        return 1
    

