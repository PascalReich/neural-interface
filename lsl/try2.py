from pylsl import StreamInlet, resolve_stream
import time
import serial
import time
import random
import pandas as pd


# set up Arduino serial port - replace with the one you are using
# ser = serial.Serial('COM4', 9600)

# resolve an EMG stream on the lab network and notify the user
print("Looking for an EMG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])
#inlet_ch2 = StreamInlet(streams[1])
print("EMG stream found!")

# initialize time threshold and variables for storing time
thres = 500
prev_time = 0

cur_step = 0
cur_word = ""
termBank = ["LEFT", "RIGHT", "UP", "DOWN"]

next_display = time.time() + 15

recording_end = 0
recording = False
recording_data = []

while cur_step < 10:

    # get EMG data sample and its timestamp
    samples, timestamp = inlet.pull_sample()

    if recording == True:
        if time.time() > recording_end:
            recording = False
            print("\n\n\n\n\n\n\n\n\n\n\n\n")
        else:
            samples.append(cur_word)
            recording_data[cur_step].append(samples)

    if time.time() > next_display:
        next_display = time.time() + 15
        cur_word = random.choice(termBank)
        print(cur_word)
        recording_data.append([])
        cur_step += 1
        recording_end = time.time() + 2

print(recording_data)
df = pd.DataFrame(recording_data)
df.to_csv('recording.csv')
