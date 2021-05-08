import imageio
from Audio import *
from operator import truediv
import numpy as np
from Warp import *

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
    out_fps=self.sampling_rate
    self.writer = imageio.get_writer(r"C:\Users\artur\Desktop\FPI\final\resultado.mp4", 'ffmpeg', macro_block_size = None, fps = out_fps)
 
	def getWarpedVideo(self, target_audio):
		source_beats = self.audio.getBeats()
		target_beats = target_audio.getBeats()
	
		warp = Warp(source_beats, target_beats)
		
		sampling_rate = self.sampling_rate
		duration = self.getDuration()
		old_frame_time = truediv(1.0, self.sampling_rate)
		
		target_start = target_beats[0]
		lead = min(target_start, 0)
		target_start = target_start - lead
		
		last_index = min(len(source_beats), len(target_beats) - 1)
		target_end = target_beats[last_index]

		target_duration = target_end - target_start
		
		print("target start: {}\ntarget end: {}\ntarget duration: {}".format(target_start, target_end, target_duration))
		
		new_n_samples = target_duration * sampling_rate
			
		target_start_times = np.linspace(target_start, target_end, num=int(new_n_samples), endpoint=False)
		
		unwarped_target_times = []
			
		for st in target_start_times:
		 	unwarped_target_times.append(warp.warpFunc(st))
    
    frame_index_floats = np.true_divide(np.array(unwarped_target_times), old_frame_time);

		self.openVideoWriter()
  
		for fr in range(len(frame_index_floats)):
			try:
				new_frame = self.getFrame(frame_index_floats[fr])
