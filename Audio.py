import librosa

class Audio():
	def __init__(self, path):
		if (path):
			self.path = path
			self.loadAudio(path)

	def loadAudio(self, path):
		stream, sampling_rate = librosa.load(path, sr=None, mono=True)
		self.stream = stream
		self.sampling_rate = sampling_rate
		print("Loaded stream and sampling_rate for {}".format(self.path))

	def getBeats(self):
		tempo, beats = librosa.beat.beat_track(self.stream, self.sampling_rate)
		self.beats = beats
		self.tempo = tempo
		print("Loaded beats and tempo for {}".format(self.path))
		return beats

	def getOnsets(self):
		onsets = librosa.onset.onset_strength(self.stream, self.sampling_rate)
		self.onsets = onsets
		print("Loaded onsets for {}".format(self.path))
