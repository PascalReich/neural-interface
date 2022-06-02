
from tensorflow.keras import Sequential
from tensorflow.keras.layers import *
from scipy.signal import butter, lfilter
import pandas as pd
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import load_model
from scipy.signal import butter, lfilter, iirnotch


#my_data = np.array(pd.read_csv("test.csv").values)
my_data = np.genfromtxt('out/test-1649010014.785578.csv', delimiter='\t')
# print(my_data)


def filter_emg(dataset):
  bpf = butter(4, [2/(fs/2), 45/(0.5*fs)], btype='band')
  nf = iirnotch(60/(fs/2),30)
  lfilter(nf[0], nf[1], lfilter(bpf[0],bpf[1], dataset))
  
def feature_normalize(dataset):
    return (dataset - np.mean(dataset, axis=0))/np.std(dataset, axis=0)

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
    my_data[:, 5], lowcut, highcut, fs, order=6)
"""
"""
my_data[:, 2] = filter_emg(
    my_data[:, 2])
my_data[:, 3] = filter_emg(
    my_data[:, 3])
my_data[:, 4] = filter_emg(
    my_data[:, 4])
my_data[:, 5] = filter_emg(
    my_data[:, 5])


my_data[:, 2] = feature_normalize(
    my_data[:, 2])
my_data[:, 3] = feature_normalize(
    my_data[:, 3])
my_data[:, 4] = feature_normalize(
    my_data[:, 4])
my_data[:, 5] = feature_normalize(
    my_data[:, 5])"""

# print(my_data.shape)

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
        # print(currentImageTrimmed.shape)
        currentImageTrimmed = np.vsplit(
            currentImageTrimmed, ([imageLength]))[0]
        if currentImageTrimmed.shape[0] < imageLength:
            print("ERROR: Invalid Image at currentWord = " + str(currentWord))
            exit(1)
        imageDirectory = np.dstack((imageDirectory, currentImageTrimmed))
        answerDirectory = np.vstack((answerDirectory, currentLine[1]))
        # print(str(imageDirectory.shape) + "\n")
        currentImage = np.zeros(4)
        currentWord = currentLine[0]
    lineIndex += 1

imageDirectory = np.transpose(imageDirectory, (2, 0, 1))
imageDirectory = np.delete(imageDirectory, 0, 0)
answerDirectory = np.delete(answerDirectory, 0, 0)
answerDirectory = to_categorical(answerDirectory)

# print(answerDirectory)

X_train, X_test, y_train, y_test = train_test_split(
    imageDirectory, answerDirectory, test_size=0.2)

y_train = np.argmax(y_train, axis=1)
y_test = np.argmax(y_test, axis=1)

# Build Model
model = Sequential()
#"""
# model.add(tf.keras.layers.experimental.preprocessing.Rescaling(1. / 4, input_shape=(imageLength, 4)))
model.add(Conv1D(64, 7, activation='relu', input_shape=(imageLength, 4)))
model.add(Dropout(0.25))
model.add(MaxPooling1D(3))
model.add(Conv1D(128, 5, activation='relu'))
model.add(Dropout(0.25))
model.add(MaxPooling1D(3))
model.add(GlobalAveragePooling1D())
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))

model.add(Dense(4, activation='softmax'))
# """

"""
model = Sequential()
model.add(Conv1D(40, 10, strides=2, padding='same', activation='relu', input_shape=(imageLength, 4)))
model.add(Dropout(0.2))
model.add(MaxPooling1D(3))
model.add(Conv1D(40, 5, strides=2, padding='same', activation='relu'))
model.add(Dropout(0.2))
model.add(MaxPooling1D(3))
model.add(Conv1D(40, 4, strides=1, padding='same', activation='relu'))
model.add(Dropout(0.2))
model.add(MaxPooling1D(3))
model.add(GlobalAveragePooling1D())
model.add(Dense(50, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(4, activation='softmax'))
"""

model.summary()

model.compile(loss='SparseCategoricalCrossentropy',
              #optimizer=tf.keras.optimizers.SGD(learning_rate=0.001),
              optimizer="adam",
              metrics=['accuracy'])

model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath="models/tom3",
    monitor= 'val_accuracy',
    verbose=0, # set to zero if it spams, but it tells u when it saves
    save_best_only=True,
    mode='auto'
)

early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_accuracy',
    patience=0
)

# Train Model
model.fit(X_train, y_train, validation_data=(
    X_test, y_test), batch_size=100, epochs=100,
          callbacks = [model_checkpoint_callback])


model = load_model("models/tom3")

y_pred = np.argmax(model.predict(X_test), axis=1) # Predictions
y_true = y_test # np.argmax(y_test, axis=1) # Ground truth

print(y_true)

# Display Confusion Matrix:
confusion_mtx = tf.math.confusion_matrix(y_true, y_pred) 
plt.figure(figsize=(10, 8))
sns.heatmap(confusion_mtx, annot=True, fmt='g')
plt.xlabel('Prediction')
plt.ylabel('Label')
plt.show()

# model.save('models/tom3')