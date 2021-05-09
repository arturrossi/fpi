from operator import truediv
import math

class Warp:
	def __init__(self, source_beats, target_beats):
		self.func = 'quad'
		self.warpFunc = self.getWarpFunction(source_beats, target_beats)
		
	def quadraticFunction(self, t, f_neighbors, t_neighbors):
		from_event_gap = f_neighbors[1] - f_neighbors[0]
		t_progress = t - f_neighbors[0]
		
		if (from_event_gap == 0):
			return
		
		progress_fraction = truediv(t_progress, from_event_gap)
		
		next_weight = math.pow(progress_fraction, 2)
	
		return (next_weight * t_neighbors[1]) + ((1.0 - next_weight) * t_neighbors[0])
	
	def getWarpFunction(self, source, target):
		start_time = min(source[0], target[0])
		
		n_events = min(len(source), len(target))
		
		f_events = source[:n_events]
		t_events = target[:n_events]
		
		def rfunc(t):
			next_f_event_index = n_events - 1
			for e in range(n_events):
				if (t < f_events[e]):
					next_f_event_index = e
					break
			
			if (next_f_event_index == 0):
				from_event = f_events[0] - start_time
				to_event = t_events[0] - start_time
				return self.quadraticFunction(t, [from_event, f_events[0]], [to_event, t_events[0]])
			
			else:
				return self.quadraticFunction(t, [f_events[next_f_event_index - 1], f_events[next_f_event_index]], [t_events[next_f_event_index - 1], t_events[next_f_event_index]])
			
		return rfunc
	
	