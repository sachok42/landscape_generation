import numpy as np


def flatten(array: list):
	return np.array(array).flatten().tolist()

def image_from_map(worldmap, filename="output.png"):
	picture_array = [flatten([pixel.color() for pixel in line]) for line in worldmap]
	png.from_array(picture_array, 'RGB').save(filename)
