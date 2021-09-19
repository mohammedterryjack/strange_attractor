from src.strange_attractor import StrangeAttractor
from utils.coordinate import Coordinate

initial = Coordinate(1.,-1.,1.)
chaos = StrangeAttractor()
path = chaos.get_trajectory(initial,steps=200)
chaos.display_trajectory(list(path))