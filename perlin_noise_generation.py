from WorldMap import WorldMap
import math
import random

def perlin_noise_generation(height, width):
	worldmap = WorldMap(height, width, zeroing=True)
	diviser = 0
	for i in range(math.ceil(math.log(height)) + 1):
		diviser += 1
		for by in range(math.ceil(height / (2 ** i))):
			for bx in range(math.ceil(width / (2 ** i))):
				mod = random.randint(0, 255)
				for k in range(2 ** i):
					y = by * (2 ** i) + k
					if y > len(worldmap):
						continue
					for g in range(2 ** i):
						x = bx * (2 ** i) + g
						if x > len(worldmap.map[0]):
							continue
						worldmap.map[y][x].height += mod

	for line in worldmap.map:
		for pixel in line:
			pixel.height //= diviser

	return worldmap

def main():
	worldmap = perlin_noise_generation(1024, 1024)
	print("perlin done")
	worldmap.render("perlin_noise_raw.png")
	worldmap.anti_alising(4)
	print("anti_alising done")
	worldmap.render("perlin_noise_alised.png")
	worldmap.export_file("perlin_noise_1024x1024.txt")

if __name__ == '__main__':
	main()