import librosa
import librosa.display
import pandas as pd
from os import listdir
from os.path import isfile, join

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
# 
# sns.set(style="darkgrid")
# 
# ize = pd.DataFrame(selectedTargets,  columns =['Sense']) 
# ax = sns.countplot(x="Sense", data=ize)

indexes[0]
preprocessed_df.iloc[indexes[0]]

selected = preprocessed_df.iloc[indexes]
selected

# endregion

selected.columns

def extract_information(df):
    audio_files = [i.replace("TextGrid", "wav") for i in df['Source']]
    
    data_tuples = list(zip(audio_files, df['Speaking'], df['Xmin'], df['Xmax'], df['Label'], df['Encoded label'], df['y']))
    new_df = pd.DataFrame(data_tuples, columns=['Source', 'Speaking', 'Xmin', 'Xmax', 'Label', 'Encoded label', 'Y'])
    
    return new_df

prepared_df = extract_information(selected)
prepared_df

def extract_features(file, start, duration):

    # Load 5 seconds of a file, starting 15 seconds in  
    # y, sr = librosa.load(filename, offset=15.0, duration=5.0)

    # Loads the audio file as a floating point time series and assigns the default sample rate
        # Sample rate is set to 22050 by default
    X, sample_rate = librosa.load(file, res_type='kaiser_fast', offset=start, duration=duration)

    # Generate Mel-frequency cepstral coefficients (MFCCs) from a time series 
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)

    # Generates a Short-time Fourier transform (STFT) to use in the chroma_stft
    stft = np.abs(librosa.stft(X))

    # Computes a chromagram from a waveform or power spectrogram.
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)

    # Computes a mel-scaled spectrogram.
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)

    # Computes spectral contrast
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)

    # Computes the tonal centroid features (tonnetz)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)

    return mfccs, chroma, mel, contrast, tonnetz


start = prepared_df['Xmin'].tolist()[1]
end = prepared_df['Xmax'].tolist()[1]
duration = end - start

start
end
duration

path = 'audio_files/' + prepared_df['Source'].tolist()[1]
path
X, sample_rate = librosa.load(path, res_type='kaiser_fast', offset=start, duration=duration)
X
sample_rate

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

    mfccs, chroma, mel, contrast, tonnetz = extract_features(path, start, duration)

    MFCCs.append(mfccs)
    chromas.append(chroma)
    mels.append(mel)
    contrasts.append(contrast)
    tonnetzs.append(tonnetz)

MFCCs
chromas
mels
contrasts
tonnetzs

prepared_df['MFCCs'] = MFCCs
prepared_df['chromas'] = chromas
prepared_df['mels'] = mels
prepared_df['contrasts'] = contrasts
prepared_df['tonnetzs'] = tonnetzs

prepared_df