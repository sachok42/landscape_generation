import math
import json
from earth_levels import earth_levels


class MapPixel:
	def __init__(self, arg1): # attribute_dict or height
		self.continent = 0
		self.humidity = 0
		self.plate = 0
		self.mountain_mod = 0
		if type(arg1) is dict:
			# print(f"dict_initializing dict is {arg1}")
			for key, value in arg1.items():
				setattr(self, key, value)
		elif type(arg1) is int or type(arg1) is float:
			self.height = arg1
			# self.humidity = 0
		else:
			print(arg1)
			raise Exception

	def change_height(self, value):
		self.height += value
		self.height = min(math.floor(abs(self.height)), 255)

	def color(self):
		height = abs(min(self.height + self.mountain_mod, 255))
		color = [0, 0, 255]
		for level, new_color in earth_levels:
			if height >= level:
				color = new_color
				break

		return color

	def set_continent(self, continent):
		self.continent = continent

	def is_land(self):
		return self.height > earth_levels[-1][0]

	def is_sea(self):
		return not self.is_land()

	def to_dict(self):
		return self.__dict__

	def _default(self, obj):
		return getattr(obj.__class__, "to_json", _default.default)(obj)

	def sinking(self):
		if self.is_land():
			self.height -= 140

	def mountainification(self, value):
		if self.mountain_mod > value:
			return False
		self.mountain_mod = value
		return True