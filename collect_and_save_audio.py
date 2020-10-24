import pandas as pd
import os
import librosa
import librosa.display
from os import listdir
from os.path import isfile, join

audio_path = 'c:/Users/hanna/Documents/BME/DipTerv_Implementation/diplomamunka/audio_files/'
audio_files = [f for f in listdir(audio_path) if isfile(join(audio_path, f))]
audio_files

path = os.getcwd()
path += '\\audio_files\\'

audio_df = pd.DataFrame()

for i in audio_files:
    temp_path = path + i
    data, sr = librosa.load(temp_path)

    temp_df = pd.DataFrame()
    temp_df["file name"] = i
    temp_df["data"] = [data]
    temp_df["sr"] = sr

    audio_df = pd.concat([audio_df, temp_df]).reset_index(drop = True)

len(audio_files)

data, sr = librosa.load('c:/Users/hanna/Documents/BME/DipTerv_Implementation/diplomamunka/audio_files/0001.wav')
data
len(data)
sr

asd = data.tolist() 
asd

temp_df = pd.DataFrame()
temp_df["file name"] = '0001.wav'
temp_df["data"] = [data]
temp_df["sr"] = sr

temp_df

asd = temp_df["data"][0]

for i in audio_files:
    

audio_df