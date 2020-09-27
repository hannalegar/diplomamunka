#region imports

import methods
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Embedding
from keras.layers import Dense
from keras.layers.recurrent import LSTM
from keras.preprocessing.text import Tokenizer

#endregion

preprocessed_df = pd.read_excel("preprocessed.xlsx", sheet_name="Sheet1")
preprocessed_df

# region refine the dataset

preprocessed_df.head(5)

atLeastFive_indexes = []
atLeastFive_indexes = [i for i in range(len(preprocessed_df['Stop word filtered text'])) if len(methods.stringarray_to_array(preprocessed_df['Stop word filtered text'][i])) > 4]

min5_texts = []
min5_target = []

for i in atLeastFive_indexes:
    min5_target.append(preprocessed_df['Modified label'][i])
    min5_texts.append(methods.stringarray_to_array(preprocessed_df['Stop word filtered text'][i]))

min5_target
min5_texts

# N - Neutral, E - Other --- > Semleges - S
# L - Ironic / Satiric, P - Complaining, I - Angry / Nervous --- > Negatív - N
# V - Happy / Laughs, O - Joyful --- > Pozitív - P

# count non S targets
non_NTargets = []
non_NTargets = sum(map(lambda x : x not in "S", min5_target))
non_NTargets

# select all S target indexes
allN_X = []
allN_X = [i for i in range(len(min5_texts)) if min5_target[i] == "S"]
allN_X
len(allN_X) == len(min5_target) - non_NTargets

# select random indexes from all index
sampling_indexes = random.choices(allN_X, k = non_NTargets*2)
sampling_indexes

# select non N indexes from all index
non_N_Indexes = [i for i in range(len(min5_target)) if min5_target[i] not in "S"]
non_N_Indexes

#merge indexes
indexes = sampling_indexes + non_N_Indexes
indexes

len(non_N_Indexes) + len(sampling_indexes) == len(indexes)

# select elements 
selectedTexts = [min5_texts[i] for i in indexes]
selectedTexts

selectedTargets = [min5_target[i] for i in indexes]
selectedTargets

for i in non_N_Indexes:
    selectedTexts.append(min5_texts[i])
    selectedTargets.append(min5_target[i])

len(selectedTargets) == (len(non_N_Indexes) *2) + len(sampling_indexes)

len(sampling_indexes)
selectedTexts[1378]
selectedTargets[1378]

selectedTexts[1377]
selectedTargets[1377]

sns.set(style="darkgrid")

labels = pd.DataFrame(selectedTargets,  columns =['Sense']) 
labels

ax = sns.countplot(x="Sense", data=labels)

# selectedTexts[2000]
# selectedTargets[2000]

all_text = [methods.stringarray_to_array(i) for i in preprocessed_df['Stop word filtered text']]
# all_text.index(selectedTexts[2000])

# all_text[33573]
# preprocessed_df['Modified label'][33573]

indexes = [all_text.index(i) for i in selectedTexts]

preprocessed_df["X"][0]

ize = to_array(preprocessed_df["X"][0])
ize

X = []
for i in indexes:
    X.append(preprocessed_df["X"][i])

X = [to_array(i) for i in X ]
X = np.array(X)

# selectedTexts[0]
# selectedTargets[0]

# all_text.index(selectedTexts[0])
# all_text[8797]

# preprocessed_df['X'][8797]
# X[0]

y = [] 
y = [preprocessed_df["y"][i] for i in indexes]
y = [to_float_array(i) for i in y]
y = np.array(y)
y


# endregion

# region build the model

len(X) == len(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

X_train
X_test
y_train
y_test

embedding_vector_length = 32 

top_words = 22776

weight = [1, 2, 150]

model = Sequential() 
model.add(Embedding(top_words, embedding_vector_length, input_length=370)) 
model.add(LSTM(100)) 
model.add(Dense(3, input_dim=3, activation='relu'))
model.add(Dense(3, activation='softmax')) 
model.compile(loss="categorical_crossentropy" ,optimizer='adam', metrics=['accuracy']) 
print(model.summary()) 

model.fit(X_train, y_train, validation_data=(X_test, y_test), nb_epoch=5, batch_size=64, class_weight=weight)

scores = model.evaluate(X_test, y_test, verbose=0) 
print("Accuracy: %.2f%%" % (scores[1]*100))

# endregion