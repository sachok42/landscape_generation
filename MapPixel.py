import math

class MapPixel:
	def __init__(self, height):
		self.height = height % 256
		self.humidity = 0

	def color(self):
		height = min(math.floor(abs(self.height)), 255)
		return [height, height, height]