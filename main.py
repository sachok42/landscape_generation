from anti_alised_generation import anti_alised_generation
from WorldMap import WorldMap
from config import area_radius
import time


def main():
	worldmap = anti_alised_generation(1000, 1000, 20)
	worldmap.render("map1")
	worldmap.operation_continental_noise()
	worldmap.render("map2")
	worldmap.export_file("map_continental.txt")

if __name__ == '__main__':
	main()