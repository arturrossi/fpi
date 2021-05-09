import imageio
from operator import truediv
import numpy as np
from Audio import *
from Warp import *
from Image import *
import cv2 as ocv
import scipy as sp
import moviepy.editor as mpy
from moviepy.audio.AudioClip import AudioArrayClip as MPYAudioArrayClip


class Video:
    def __init__(self, path=None):
        self.path = path
        self.loadFile(path)

    def loadFile(self, path):
        self.reader = imageio.get_reader(path, 'ffmpeg')
        self.metadata = self.reader.get_meta_data()
        self.sampling_rate = self.metadata['fps']
        self.num_frames = self.reader.count_frames()
        self.audio = Audio(path)
        print("Loaded video and audio from file {}".format(self.path))

    def getDuration(self):
        return truediv(self.num_frames, self.sampling_rate)

    def openVideoWriter(self):
        out_fps = self.sampling_rate
        self.writer = imageio.get_writer(
            r"C:\Users\artur\Desktop\fpi\resultado2.mp4", 'ffmpeg', macro_block_size=None, fps=out_fps)

    def closeVideoWriter(self):
        self.writer.close()
        self.writer = None

    def writeFrame(self, img):
        if self.writer.closed:
            print('ERROR: Vid writer object is closed.')
        else:
            self.writer.append_data(img.astype(np.uint8))

    def getImageFromFrame(self, i):
        rimage = Image(data=self.getFrame(i))
        return rimage

    def readFrameBasic(self, i):
        fi = i
        if(fi < 0):
            fi = 0
        if(fi > (self.num_frames-1)):
            fi = (self.num_frames-1)
        return np.asarray(self.reader.get_data(int(fi)))

    def getFrame(self, f):
        return self.readFrameBasic(round(f))

    def quadratic(self, t, source_neighbors, target_neighbors):
        source_event_gap = source_neighbors[1] - source_neighbors[0]
        t_progress = t - source_neighbors[0]

        if (source_event_gap == 0):
            return 0

        if (t <= source_neighbors[0]):
            return 0

        progress_frac = truediv(t_progress, source_event_gap)

        return math.pow(progress_frac, 2)

    def getWarpedVideo(self, target_beats, source_beats):
        n_events = min(len(target_beats), len(source_beats))
        last_index_target_beats = len(target_beats) - 1
        last_index_source_beats = len(source_beats) - 1

        print("Target audio number of beats: {}".format(len(target_beats)))
        print("Source video number of beats: {}".format(len(source_beats)))
        print("Number of events: {}".format(n_events))

        new_source_beats = []

        source_events = source_beats[:n_events]
        target_events = target_beats[:n_events]

        target_start_time = target_beats[0] - min(target_beats[0], 0)
        target_end_time = source_beats[min(
            len(source_beats), len(target_beats)) - 1]

        print("Min between target audio and source video: {}".format(min(
            len(source_beats), len(target_beats))))

        target_duration = target_end_time - target_start_time

        print("Target start time: {}\nTarget end time: {}\nTarget duration: {}".format(target_start_time, target_end_time, target_duration))

        new_n_samples = target_duration

        target_start_times = np.linspace(
            target_start_time, target_end_time, num=int(new_n_samples), endpoint=False)

        start_cap_time = min(target_beats[0], source_beats[0])

        for t in target_start_times:
            next_f_event_index = n_events - 1
            for e in range(n_events):
                if (t < source_events[e]):
                    next_f_event_index = e
                    break

            if (next_f_event_index == 0):
                source_neighbors = [source_events[0] -
                                    start_cap_time, source_events[0]]
                target_neighbors = [target_events[0] -
                                    start_cap_time, target_events[0]]
                new_source_beats.append(self.quadratic(
                    t, source_neighbors, target_neighbors))
            else:
                source_neighbors = [
                    source_events[next_f_event_index - 1], source_events[next_f_event_index]]
                target_neighbors = [
                    target_events[next_f_event_index - 1], target_events[next_f_event_index]]
                new_source_beats.append(self.quadratic(
                    t, source_neighbors, target_neighbors))

        old_frame_time = truediv(1.0, self.sampling_rate)

        frame_index_floats = np.true_divide(
            np.array(new_source_beats), old_frame_time)

        self.openVideoWriter()

        for nf in range(len(frame_index_floats)):
            try:
                nwfr = self.getFrame(frame_index_floats[nf])
                self.writeFrame(nwfr)
            except ValueError:
                print("VALUE ERROR ON WRITEFRAME {}".format(frame_index_floats[nf]))
                self.writeFrame(self.getFrame(math.floor(frame_index_floats[nf])))

        self.closeVideoWriter()

        output_video = self.createVideoWithAudio(
            start=target_start_time, end=target_end_time)

        print("New video duration: {}".format(output_video.getDuration()))

    def createVideoWithAudio(self, start, end):
        audio_object = Audio(r"C:\Users\artur\Desktop\fpi\doiwannaknow.mp3")
        audio_sig = audio_object.stream

        audio_duration = truediv(len(audio_sig), audio_object.sampling_rate)
        video_duration = self.getDuration()

        n_audio_samples_in_vid = int(
            math.ceil(video_duration * audio_object.sampling_rate))

        if (n_audio_samples_in_vid < len(audio_object.stream)):
            audio_sig = audio_sig[:int(n_audio_samples_in_vid)]
        else:
            if (n_audio_samples_in_vid > len(audio_object.stream)):
                nreps = math.ceil(
                    truediv(n_audio_samples_in_vid, len(audio_object.stream)))
                audio_sig = np.tile(audio_sig, (int(nreps)))
                audio_sig = audio_sig[:int(n_audio_samples_in_vid)]
        reshapex = audio_sig.reshape(len(audio_sig), 1)
        reshapex = np.concatenate((reshapex, reshapex), axis=1)
        audio_clip = MPYAudioArrayClip(
            reshapex, fps=audio_object.sampling_rate)

        video_clip = mpy.VideoFileClip(
            r"C:\Users\Artur\Desktop\fpi\resultado2.mp4", audio=True)
        video_clip = video_clip.set_audio(audio_clip)
        self.MPYWriteVideoFile(video_clip, r"C:\Users\Artur\Desktop\fpi\resultado_som.mp4",
                          codec="libx264", write_logfile=False)

        return Video(r"C:\Users\Artur\Desktop\fpi\resultado_som.mp4")

    def MPYWriteVideoFile(self, mpyclip, filename, **kwargs):
        return mpyclip.write_videofile(filename=filename, temp_audiofile=r"C:\Users\Artur\Desktop\fpi\temp_resultado_som.mp4", audio_codec='aac', **kwargs)
