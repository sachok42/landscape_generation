from config import delta, area_radius, difference_limit, min_island, mountain_delta, mountain_radius
from MapPixel import MapPixel
from utilities import *
import png
import random
import time
from log_config import create_logger
import pandas
import json
from math import sqrt
from Continent import Continent

class WorldMap:
	def __init__(self, arg1, width=None): # arg1 is either height or filename
		if type(arg1) == int and type(width) == int:
			self.height = arg1
			self.width = width
			self.map = [[None for _ in range(width)] for __ in range(self.height)]
		elif type(arg1) == str and width is None:
			self.read_file(arg1)

	def sum_height(self, x, y, radius=area_radius):
		existing_pixels = 0
		sum_height = 0
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
		return sum_height, existing_pixels

	def mean_height(self, x, y, radius=area_radius):
		sum_height, existing_pixels = self.sum_height(x, y, radius)
		if existing_pixels == 0:
			return random.randint(0, 255)
		return sum_height / existing_pixels

	def anti_alising(self, radius=area_radius):
		for y in range(len(self)):
			for x in range(len(self.map[0])):
				if abs(self.mean_height(x, y) - self.map[y][x].height) > difference_limit:
					self.predict_pixel(x, y)

	def anti_alising_geo(self, radius=area_radius):
		for y in range(len(self)):
			for x in range(len(self.map[0])):
				if abs(self.mean_height_geo(x, y) - self.map[y][x].height) > difference_limit:
					self.predict_pixel_geo(x, y)

	def tectonic_plates_generation(self, plates_number):
		self.plate_centers = [(random.randint(0, 1919), random.randint(0, 1079)) for _ in range(plates_number)]
		for y in range(len(self)):
			for x in range(self.width):
				min_distance = 1e6
				plate_number = None

				for number, cords in enumerate(self.plate_centers):
					c_x, c_y = cords
					distance = sqrt((c_x - x) ** 2 + (c_y - y) ** 2)
					if distance < min_distance:
						min_distance = distance
						plate_number = number

				self.map[y][x].plate = plate_number

	def is_plate_border(self, x, y):
		plate_number = self.map[y][x].plate
		for y in range(y - 1, y + 2):
			if y < 0 or y >= self.height:
				continue
			for x in range(x - 1, x + 2):
				if x < 0 or x >= self.width:
					continue
				if self.map[y][x].plate != plate_number:
					return True
		return False

	def product_height(self, x, y, radius=area_radius):
		existing_pixels = 0
		product_height = 1
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
				product_height *= self.map[y + i][x + j].height
				existing_pixels += 1
		return product_height, existing_pixels

	def mean_height_geo(self, x, y, radius=area_radius): # geometrical
		product_height, existing_pixels = self.product_height(x, y, radius)
		if existing_pixels == 0:
			return random.randint(0, 255)
		return product_height ** (1 / existing_pixels)

	def predict_pixel(self, x, y, radius=area_radius):
		self.map[y][x] = MapPixel(self.mean_height(x, y, radius) + random.randint(-delta, delta))

	def predict_pixel_geo(self, x, y, radius=area_radius):
		self.map[y][x] = MapPixel(self.mean_height_geo(x, y, radius) + random.randint(-delta // 2, delta // 2))

	def render(self, filename=None, radius=area_radius):
		if filename is None:
			filename = f"anti_alised_generation_{self.height}x{self.width}_radius{radius}_time{time.time()}.png"
		picture_array = [flatten([pixel.color() for pixel in line]) for line in self.map]
		for y, line in enumerate(picture_array):
			for x in range(len(line) // 3):
				if self.is_plate_border(x, y):
					for i in range(3):
						picture_array[y][x * 3 + i] = 0
		png.from_array(picture_array, 'RGB').save(f"render_archive/{filename}")

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

	def find_continents(self):
		self.visited = [[False for i in range(len(self.map[0]))] for _ in range(len(self))]
		self.continents_map = [[-1 for i in range(len(self.map[0]))] for _ in range(len(self))]
		self.continents_num = 0
		self.continents_list = [[]]

		for y in range(len(self)):
			for x in range(len(self.map[0])):
				if not self.visited[y][x] and self.map[y][x].is_land():
					# self.visited[y][x] = True
					self.dfs(x, y, self.continents_num, [(x, y)])
					self.continents_num += 1
					self.continents_list.append([])
					print(f"continent number {len(self.continents_list)} done")

		self.continents = []
		for tiles in self.continents_list:
			self.continents.append(Continent(self.map, tiles))

	# def find_seas

	def dfs(self, x, y, continent, stack):
		limit = 0
		while stack and limit < 300000:
			x, y = stack[-1]
			stack.pop()
			limit += 1
			if y >= len(self) or y < 0 or x < 0 or x >= self.width or self.visited[y][x]:
				continue
			if not self.visited[y][x] and self.map[y][x].is_land():
				self.visited[y][x] = True
				self.continents_map[y][x] = continent
				stack.append((x, y - 1))
				stack.append((x - 1, y))
				stack.append((x, y + 1))
				stack.append((x + 1, y))
				self.map[y][x].set_continent(continent)
				self.continents_list[-1].append((x, y))

	def operation_continental_noise(self):
		try:
			for continent in self.continents_list:
				if len(continent) <= min_island:
					for x, y in continent:
						self.map[y][x].sinking()
		except Exception:
			self.find_continents()
			for continent in self.continents_list:
				if len(continent) <= min_island:
					for x, y in continent:
						self.map[y][x].sinking()

	def mountains_generation(self):
		for y, line in enumerate(self.map):
			print(f"Line {y} started, mountainification")
			for x, pixel in enumerate(line):
				if self.is_plate_border(x, y):
					for dy in range(-mountain_radius, mountain_radius + 1):
						if y + dy < 0 or y + dy >= self.height:
							continue
						for dx in range(-mountain_radius, mountain_radius + 1):
							if x + dx < 0 or x + dx >= self.height:
								continue
							self.map[y + dy][x + dx].mountainification(mountain_delta / mountain_radius * (mountain_radius - max(dx, dy)))
