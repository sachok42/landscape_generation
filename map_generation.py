from MapPixel import MapPixel
import png
import random
import numpy as np
random.seed(int(input()))

def flatten(array: list):
	return np.array(array).flatten().tolist()

def generation_from_three(pixel1, pixel2, pixel3):
	height = (pixel1.height + pixel2.height + pixel3.height) / 3 + random.randint(-5, 5)
	return MapPixel(height)

def image_from_map(worldmap, filename="output.png"):
	picture_array = [flatten([pixel.color() for pixel in line]) for line in worldmap]
	png.from_array(picture_array, 'RGB').save(filename)


def main():
	height, width = map(int, input().split())
	worldmap = [[None for _ in range(width)] for _ in range(height)]

	worldmap[0][0] = MapPixel(random.randint(0, 255))
	for x in range(1, width):
		worldmap[0][x] = MapPixel(worldmap[0][x - 1].height + random.randint(-5, 5))

	for y in range(1, height):
		worldmap[y][0] = MapPixel(worldmap[y - 1][0].height + random.randint(-5, 5))

	for y in range(1, height):
		for x in range(1, width):
			worldmap[y][x] = generation_from_three(worldmap[y - 1][x], worldmap[y][x - 1], worldmap[y - 1][x - 1])

	image_from_map(worldmap)

if __name__ == '__main__':
	main()