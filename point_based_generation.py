from WorldMap import WorldMap
from config import area_radius, delta
import time
from log_config import create_logger
import random


point_based_logger = create_logger("point_based_logger", "point_based_log.log")

def point_based_generation(height, width, radius=area_radius, iterations=1):
	now = time.time()
	world = WorldMap(height, width)
	# print(len(world[0]), len(world))
	for _ in range(iterations):
		cords_list = [[(x, y) for x in range(len(world[0]))] for y in range(len(world))]
		new_cords_list = []
		for array in cords_list:
			for element in array:
				new_cords_list.append(element)
		cords_list = new_cords_list
		# cords_list = flatten(cords_list)
		# print(cords_list)
		random.shuffle(cords_list)
		for x, y in cords_list:
			# x, y = map(int, cords.split('_'))
			# print(x, y)
			world.predict_pixel(x, y, radius)
	point_based_logger.info(f"generated landscape {height}x{width} in {time.time() - now} seconds")
	return world


if __name__ == '__main__':
	for iterations_num in range(1, 1):
		for height, width in [(100, 100), (200, 200), (500, 500), (1000, 1000), (1080, 1920)]:
			now = time.time()
			world = point_based_generation(height, width, area_radius, iterations_num)
			filename = f"{height}x{width}_radius{area_radius}_iteratons{iterations_num}_delta{delta}.png"
			world.render(filename)
			# point_based_logger.info(f"generated landscape {height}x{width} in {time.time() - now} seconds")
			print(f"done with {height}x{width} {iterations_num} iterations")
