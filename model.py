#region imports

import methods
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt

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


# endregion







X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)