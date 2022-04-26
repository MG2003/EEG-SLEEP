import argparse
import time
import brainflow
import numpy as np

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds, BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams
from brainflow.exit_codes import *


def main():
    BoardShim.enable_board_logger()
    DataFilter.enable_data_logger()
    MLModel.enable_ml_logger()

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=15)

    parser.add_argument('dongle serial port(COM3, /dev/ttyUSB0…)', type=str, help='serial port', required=False, default='')
    parser.add_argument('c7:86:fd:64:9c:e0', type=str, help='mac address', required=False, default='')
 
    parser.add_argument('1', type=int, help='board id, check docs to get a list of supported boards',
                        required=True)

    args = parser.parse_args()
    params = BrainFlowInputParams()
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.timeout = args.timeout

    board = BoardShim(args.board_id, params)
    master_board_id = 1
    sampling_rate = BoardShim.get_sampling_rate(master_board_id)
    board.prepare_session()
    board.start_stream(45000, args.streamer_params)
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(5)  # recommended window size for eeg metric calculation is at least 4 seconds, bigger is better
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(int(master_board_id))
    bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, True)
    feature_vector = np.concatenate((bands[0], bands[1]))
    print(feature_vector)

    #calc sleep


    # calc concentration
    concentration_params = BrainFlowModelParams(BrainFlowMetrics.CONCENTRATION.value, BrainFlowClassifiers.KNN.value)
    concentration = MLModel(concentration_params)
    concentration.prepare()
    print('Concentration: %f' % concentration.predict(feature_vector))
    concentration.release()

    # calc relaxation
    relaxation_params = BrainFlowModelParams(BrainFlowMetrics.RELAXATION.value, BrainFlowClassifiers.REGRESSION.value)
    relaxation = MLModel(relaxation_params)
    relaxation.prepare()
    print('Relaxation: %f' % relaxation.predict(feature_vector))
    relaxation.release()


if __name__ == "__main__":
    main()