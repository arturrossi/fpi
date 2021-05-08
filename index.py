import librosa
import imageio
from Video import *

def getAudioFromVideo(path):  
  return loadAudio(path)

source_video = Video(r"C:\Users\artur\Desktop\FPI\final\speech.mp4")
target_audio = Audio(r"C:\Users\artur\Desktop\FPI\final\doiwannaknow.mp3")

source_video.getWarpedVideo(target_audio)

# def getWarp(source_events, target_events):
  


# x, sampling_rate = loadAudio(r"C:\Users\artur\Desktop\FPI\final\doiwannaknow.mp3")
# tempo, beats = getBeats(x, sampling_rate)
# onsets = getOnsets(x, sampling_rate)


# source_video_beats = getBeats(source_video_audio_x, source_video_sr)
# warp = getWarp(source_video_beats, beats)

