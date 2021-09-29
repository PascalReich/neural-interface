import tensorflow as tf
import numpy as np
from tensorflow.keras import *
from scipy.signal import butter, lfilter, iirnotch
import pandas as pd


session = pd.read_csv(folder+files[0],skiprows=6, index_col=None,header=None,
                      names=["ix","1","2","3","4","ax","ay","az","time","epoch"])



def filter_emg(dataset):
    bpf = butter(4, [2/(fs/2), 45/(0.5*fs)], btype='band')
    nf = iirnotch(60/(fs/2),30)
    lfilter(nf[0], nf[1], lfilter(bpf[0],bpf[1], dataset))

def feature_normalize(dataset):
    return (dataset - np.mean(dataset, axis=0))/np.std(dataset, axis=0)


# Load labelled EMG sessions to train on
selected = ['esic_82','cise_38','iecs_45']
x, y = np.empty((0, L, 4), np.float32), np.empty((0, 4), np.float32)
for k in selected:
    x = np.append(x,sessions[k][0],axis=0)
    y = np.append(y,sessions[k][1],axis=0)

# Downsample, shuffle and split (from sklearn.cross_validation)
x_train, x_val, y_train, y_val = train_test_split((x[:,::ds,:]), y, test_size=0.25)

# Create the network
model = Sequential()
model.add(Conv1D(40, 10, strides=2, padding='same', activation='relu', input_shape=(x_train.shape[0]//ds, 4)))
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

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Train and save results for later plotting
history[ '40 1023 523 413 50 :'+'-'.join(selected)] = model.fit(x_train, y_train,
                                                                batch_size=100, epochs=40, validation_data=(x_val,y_val))