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

	def color(self):
		if self.height > 127:
			return (0, 255, 0)
		return [0, 0, 255]

	def to_dict(self):
		return self.__dict__

	def _default(self, obj):
		return getattr(obj.__class__, "to_json", _default.default)(obj)