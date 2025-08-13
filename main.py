from anti_alised_generation import anti_alised_generation
from WorldMap import WorldMap


def main():
	worldmap = anti_alised_generation(100, 100)
	worldmap.export_file("test_dump.txt")
	worldmap.render("map1.png")
	worldmap2 = WorldMap("test_dump.txt")
	worldmap2.render("map2.png")

if __name__ == '__main__':
	main()