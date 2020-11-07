import pandas as pd
import numpy as np
import methods
import matplotlib.pyplot  as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler

prepared_df = pd.read_excel("prepared_audio_df.xlsx", sheet_name="Sheet1")
prepared_df

MFCCs = [methods.audio_to_float_array(i) for i in prepared_df['MFCCs']]
chromas = [methods.audio_to_float_array(i) for i in prepared_df['chromas']]
mels = [methods.audio_to_float_array(i) for i in prepared_df['mels']]
contrasts = [methods.audio_to_float_array(i) for i in prepared_df['contrasts']]
tonnetzs = [methods.audio_to_float_array(i) for i in prepared_df['tonnetzs']]

features_train = []
for i in range(len(MFCCs)):
    features_train.append(np.concatenate((
        MFCCs[i],
        chromas[i], 
        mels[i], 
        contrasts[i],
        tonnetzs[i]), axis=0))

len(features_train[0]) == len(MFCCs[0]) + len(chromas[0]) + len(mels[0]) + len(contrasts[0]) + len(tonnetzs[0])
len(features_train[0])

X = np.array(features_train)

y = [methods.to_float_array(i) for i in prepared_df['Y']]
y = np.asarray(y)
y

ss = StandardScaler()
X = ss.fit_transform(X)

# Build a simple dense model with early stopping and softmax for categorical classification, remember we have 30 classes
model = Sequential()
model.add(Dense(193, input_shape=(193,), activation = 'relu'))
model.add(Dropout(0.1))
model.add(Dense(128, activation = 'relu'))
model.add(Dropout(0.25))
model.add(Dense(128, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(3, activation = 'softmax'))
model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
early_stop = EarlyStopping(monitor='val_loss', min_delta=0, patience=100, verbose=1, mode='auto')

history = model.fit(X, y, batch_size=256, epochs=100)

history.history

train_accuracy = history.history['acc']
train_accuracy

val_accuracy = history.history['loss']
val_accuracy

# Set figure size.
plt.figure(figsize=(12, 8))

# Generate line plot of training, testing loss over epochs.
plt.plot(train_accuracy)
plt.plot(val_accuracy)

# Set title
plt.xlabel('Epoch', fontsize = 18)
plt.ylabel('Categorical Crossentropy', fontsize = 18)
plt.xticks(range(0,100,5), range(0,100,5))
plt.legend(fontsize = 18)
plt.show()