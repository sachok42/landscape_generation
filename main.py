from anti_alised_generation import anti_alised_generation
from WorldMap import WorldMap
from config import area_radius
import time


def main():
	# worldmap = anti_alised_generation(1000, 1000, 20)
	# worldmap.tectonic_plates_generation(100)
	# worldmap.mountains_generation()
	# worldmap.operation_continental_noise()
	# worldmap.render("tectonic_map2.png")
	# worldmap.export_file("tectonic_map2.txt")
	# worldmap.render("map1")
	# worldmap.operation_continental_noise()
	# worldmap.render("map2")
	# worldmap.export_file("map_continental.txt")
	worldmap = WorldMap("map_continental.txt")
	worldmap.tectonic_plates_generation(100)
	worldmap.mountains_generation()
	worldmap.render("map3.png")

if __name__ == '__main__':
	main()