#region imports

import pandas as pd
import numpy as np
import methods

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
    filtered_sentence = methods.stop_word_filtering(s)
    if len(filtered_sentence) == 0:
        filtered_sentence = np.NaN
    filtered_texts.append(filtered_sentence)

text_and_label_df2['Stop word filtered text'] = filtered_texts
text_and_label_df2

#endregion