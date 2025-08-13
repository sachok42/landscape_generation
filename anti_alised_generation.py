from WorldMap import WorldMap
from config import area_radius
from point_based_generation import point_based_generation
import time


def anti_alised_generation(height, width, radius=area_radius):
	worldmap = point_based_generation(height, width, radius)
	worldmap.anti_alising()
	worldmap.render()
	return worldmap

def main():
	anti_alised_generation(1080, 1920)

if __name__ == '__main__':
	main()