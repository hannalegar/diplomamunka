import librosa
import librosa.display
from os import listdir
from os.path import isfile, join

audio_path = 'c:/Users/hanna/Documents/BME/DipTerv_Implementation/diplomamunka/audio_files/'
audio_files = [f for f in listdir(audio_path) if isfile(join(audio_path, f))]
audio_files


data, sr = librosa.load(audio_path + '0989.wav')
