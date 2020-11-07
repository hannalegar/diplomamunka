import pandas as pd
import random
import methods

preprocessed_df = pd.read_excel("preprocessed.xlsx", sheet_name="Sheet1")
preprocessed_df.reset_index(drop=True, inplace=True)
preprocessed_df

# region select indexes
labels = preprocessed_df['Modified label']
labels

# count non S targets
non_NTargets = sum(map(lambda x : x not in "S", labels))
non_NTargets

# select all S target indexes
allN_X = []
allN_X = [i for i in range(len(labels)) if labels[i] == "S"]
allN_X
len(allN_X)

sampling_indexes = random.choices(allN_X, k = non_NTargets)
sampling_indexes

non_N_Indexes = [i for i in range(len(labels)) if labels[i] not in "S"]
non_N_Indexes

indexes = sampling_indexes + non_N_Indexes
indexes

# selectedTargets = [labels[i] for i in indexes]
# selectedTargets
 
# sns.set(style="darkgrid")
 
# ize = pd.DataFrame(selectedTargets,  columns =['Sense']) 
# ax = sns.countplot(x="Sense", data=ize)

indexes[0]
preprocessed_df.iloc[indexes[0]]

selected = preprocessed_df.iloc[indexes]
selected

# endregion

selected.columns

prepared_df = methods.extract_information(selected)
prepared_df

MFCCs = []
chromas = []
mels = []
contrasts = []
tonnetzs = []

for i in range(len(selected['Source'])):
    path = 'audio_files/' + prepared_df['Source'].tolist()[i]
    start = prepared_df['Xmin'].tolist()[i]
    end = prepared_df['Xmax'].tolist()[i]
    duration = end - start

    mfccs, chroma, mel, contrast, tonnetz = methods.extract_features(path, start, duration)

    MFCCs.append(mfccs)
    chromas.append(chroma)
    mels.append(mel)
    contrasts.append(contrast)
    tonnetzs.append(tonnetz)

#MFCCs
#chromas
#mels
#contrasts
#tonnetzs

prepared_df['MFCCs'] = MFCCs
prepared_df['chromas'] = chromas
prepared_df['mels'] = mels
prepared_df['contrasts'] = contrasts
prepared_df['tonnetzs'] = tonnetzs

prepared_df

prepared_df.to_excel("prepared_audio_df.xlsx") 