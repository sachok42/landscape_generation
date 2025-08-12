import math

class MapPixel:
	def __init__(self, height):
		self.height = min(math.floor(abs(height)), 255)
		self.humidity = 0

	def color(self):
		if self.height > 127:
			return (0, 255, 0)
		return [0, 0, 255]