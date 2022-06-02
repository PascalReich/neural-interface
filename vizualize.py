import pandas as pd
import numpy as np
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
import time

#my_data = np.array(pd.read_csv("test.csv").values)
my_data = np.genfromtxt('out/test-1637470233.205806.csv', delimiter='\t')
#print(my_data)


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


nsamples = my_data[:, 1].shape[0]
T = nsamples/400
t = np.linspace(0, T, nsamples, endpoint=False)
fs = 400.0
lowcut = 4.0
highcut = 50.0
"""
my_data[:, 2] = butter_bandpass_filter(
    my_data[:, 2], lowcut, highcut, fs, order=6)
my_data[:, 3] = butter_bandpass_filter(
    my_data[:, 3], lowcut, highcut, fs, order=6)
my_data[:, 4] = butter_bandpass_filter(
    my_data[:, 4], lowcut, highcut, fs, order=6)
my_data[:, 5] = butter_bandpass_filter(
    my_data[:, 5], lowcut, highcut, fs, order=6)"""


print(my_data.shape)

lineIndex = 0
currentWord = 0
imageLength = 110
currentImage = np.zeros(4)
imageDimensions = (imageLength, 4)
imageDirectory = np.zeros(imageDimensions)
answerDirectory = np.zeros(1)

while lineIndex < my_data.shape[0]:
    currentLine = np.array(my_data[lineIndex])
    if int(currentLine[0]) == currentWord:
        currentImage = np.vstack((currentImage, currentLine[2:]))
    else:
        # print(currentImageTrimmed.shape)
        currentImageTrimmed = np.delete(currentImage, 0, 0)
        #print(currentImageTrimmed.shape)
        currentImageTrimmed = np.vsplit(
            currentImageTrimmed, ([imageLength]))[0]
        if currentImageTrimmed.shape[0] < imageLength:
            print("ERROR: Invalid Image at currentWord = " + str(currentWord))
            exit(1)
        imageDirectory = np.dstack((imageDirectory, currentImageTrimmed))
        answerDirectory = np.vstack((answerDirectory, currentLine[1]))
        #print(str(imageDirectory.shape) + "\n")
        currentImage = np.zeros(4)
        currentWord = currentLine[0]
    lineIndex += 1

imageDirectory = np.transpose(imageDirectory, (2, 0, 1))
imageDirectory = np.delete(imageDirectory, 0, 0)
answerDirectory = np.delete(answerDirectory, 0, 0)
print(imageDirectory.shape)

fig, axs = plt.subplots(3, 3, squeeze=True)

axs = axs.flatten()
for i in range(9):
    df = pd.DataFrame(
        imageDirectory[i], columns=["A", "B", "C", "D"]
    )

    df = df.cumsum()

    axs[i].set_title(answerDirectory[i])
    df.plot(ax=axs[i], legend=None);

    # plt.legend(loc='best');

plt.show()

