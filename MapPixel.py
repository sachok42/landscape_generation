import math
import json

class MapPixel:
	def __init__(self, arg1): # attribute_dict or height
		if type(arg1) is dict:
			# print(f"dict_initializing dict is {arg1}")
			for key, value in arg1.items():
				setattr(self, key, value)
		elif type(arg1) is int or type(arg1) is float:
			self.height = min(math.floor(abs(arg1)), 255)
			self.humidity = 0
		else:
			print(arg1)
			raise Exception

		self.continent = 0

	def color(self):
		if self.height > 230:
			return [96, 96, 96]
		elif self.height > 220:
			return [192, 192, 192]
		elif self.height > 200:
			return [0, 102, 0]
		elif self.height > 150:
			return [51, 251, 51]
		elif self.height > 140:
			return [255, 255, 0]
		return [0, 0, 255]

	def set_continent(self, continent):
		self.continent = continent

	def is_land(self):
		return self.height > 140

	def to_dict(self):
		return self.__dict__

	def _default(self, obj):
		return getattr(obj.__class__, "to_json", _default.default)(obj)

	def sinking(self):
		if self.is_land():
			self.height -= 140