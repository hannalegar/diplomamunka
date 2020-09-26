#region imports

import methods
import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder

#endregion

text_and_label_df2 = pd.read_excel("text_and_label_df.xlsx", sheet_name="Sheet1")
text_and_label_df2

#region split sentences into words and set stop words

texts = text_and_label_df2['Text']

splitted_texts = [] 
for i in texts:
    splitted_texts.append(methods.split_senteces_into_words(i))
text_and_label_df2['Splitted text'] = splitted_texts

filtered_texts = []
for s in splitted_texts:
    filtered_texts.append(methods.stop_word_filtering(s))

text_and_label_df2['Stop word filtered text'] = filtered_texts
text_and_label_df2.head(15)

#endregion

#region tokenize texts

t = Tokenizer()
t.fit_on_texts(text_and_label_df2['Text'])

encoded_texts = []
encoded_texts = [methods.encode(i, t) for i in text_and_label_df2['Stop word filtered text'].tolist()]

# reverse_word_map = dict(map(reversed, t.word_index.items()))
# 
# for i in range(0, 10):
#     print(text_and_label_df2['Stop word filtered text'][i])
#     print(encoded_texts[i])
#     methods.decode(encoded_texts[i], reverse_word_map)

text_and_label_df2['Encoded text'] = encoded_texts

#endregion

#region encode label

original_labels = text_and_label_df2['Label']
new_labels = []

for i in range(len(original_labels)):
    if original_labels[i] in "NER":# N - Neutral, E - Other
        new_labels.append("S") # Semleges --> S
    if original_labels[i] in "LPI": # L - Ironic / Satiric, P - Complaining, I - Angry / Nervous
        new_labels.append("N") # Negatív --> N
    if original_labels[i] in "VO": # V - Happy / Laughs, O - Joyful
        new_labels.append("P") # Pozitív --> P

text_and_label_df2['Modified label'] = new_labels

encoded_labels = []
encoded_labels = [methods.char_toNum_switcher.get(i) for i in new_labels]
encoded_labels

text_and_label_df2['Encoded label'] = encoded_labels

#endregion

#region encoding labels and text

max_textsize = len(max(text_and_label_df2['Text'], key=len)) 

X = []
X = sequence.pad_sequences(text_and_label_df2['Encoded text'], maxlen = max_textsize)

text_and_label_df2['X'] = X.tolist()

# reverse_word_map = dict(map(reversed, t.word_index.items()))
# methods.decode(text_and_label_df2['X'][0][-2:], reverse_word_map)

encoder = LabelEncoder()
encoder.fit(encoded_labels)
y = np_utils.to_categorical(encoded_labels)

text_and_label_df2['y'] = y.tolist()

#end region

text_and_label_df2.head(10)
text_and_label_df2.to_excel("preprocessed.xlsx")