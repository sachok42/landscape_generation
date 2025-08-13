from config import delta, area_radius, difference_limit
from MapPixel import MapPixel
from utilities import *
import png
import random
import time
from log_config import create_logger
import pandas
import json


class WorldMap:
	def __init__(self, arg1, width=None): # arg1 is either height or filename
		if type(arg1) == int and type(width) == int:
			self.height = arg1
			self.width = width
			self.map = [[None for _ in range(width)] for __ in range(self.height)]
		elif type(arg1) == str and width is None:
			self.read_file(arg1)

	def mean_height(self, x, y, radius=area_radius):
		sum_height = 0
		existing_pixels = 0

		for i in range(-radius, radius + 1):
			if y + i >= self.height or y + i < 0:
				continue
			for j in range(-radius, radius + 1):
				if x + j >= self.width or x + j < 0:
					continue
				if i == j == 0:
					continue
				if not self.map[y + i][x + j]:
					continue
				sum_height += self.map[y + i][x + j].height
				existing_pixels += 1

		if existing_pixels == 0:
			return random.randint(0, 255)
		return sum_height / existing_pixels

	def anti_alising(self, radius=area_radius):
		for y in range(len(self)):
			for x in range(len(self.map[0])):
				if abs(self.mean_height(x, y) - self.map[y][x].height) > difference_limit:
					self.predict_pixel(x, y)

	def predict_pixel(self, x, y, radius=area_radius):
		# if self.Pixel != None:
		# 	return
		self.map[y][x] = MapPixel(self.mean_height(x, y, area_radius) + random.randint(-delta, delta))

	def render(self, filename=None):
		if filename is None:
			filename = f"anti_alised_generation_{self.height}x{self.width}_radius{area_radius}_time{time.time()}.png"
		picture_array = [flatten([pixel.color() for pixel in line]) for line in self.map]
		png.from_array(picture_array, 'RGB').save(filename)

	def export_file(self, filename):
		export_map = [[pixel.to_dict() for pixel in line] for line in self.map]
		dump = json.dumps(export_map)
		with open(filename, 'w') as file:
			file.write(dump)

	def read_file(self, filename):
		dump = None
		with open(filename, 'r') as file:
			dump = file.read()
		import_map = json.loads(dump)
		self.map = [[MapPixel(pixel) for pixel in line] for line in import_map]
		self.height = len(self.map)
		self.width = len(self.map[0])

	def __len__(self):
		return self.height

	def __getitem__(self, arg):
		return self.map[arg]

