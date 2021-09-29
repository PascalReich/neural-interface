from pyOpenBCI import OpenBCIGanglion
from pylsl import StreamInfo, StreamOutlet, ContinuousResolver
import numpy as np
import random
import time

SCALE_FACTOR_EEG = ((4500000)/24/(2**23-1))/1.5 #uV/count

print("Creating LSL stream for EEG. \nName: OpenBCIEEG\nID: OpenBCItestEEG\n")

info_eeg = StreamInfo('OpenBCIEEG', 'EEG', 4, 250, 'float32', 'OpenBCItestEEG')

outlet_eeg = StreamOutlet(info_eeg)

info = StreamInfo('MyMarkerStream', 'Markers', 1, 0, 'string', 'myuidw43536')
# next make an outlet
outlet = StreamOutlet(info)
markernames = ['Marker']


def lsl_streamers(sample):
    outlet_eeg.push_sample(np.array(sample.channels_data)*SCALE_FACTOR_EEG)
    outlet.push_sample([markernames[0]])
    print(np.array(sample.channels_data)*SCALE_FACTOR_EEG)

    board = OpenBCIGanglion(mac='E0:40:DA:FF:A2:F7')

    board.start_stream(lsl_streamers)