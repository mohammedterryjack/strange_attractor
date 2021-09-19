from typing import List 
from matplotlib.pyplot import figure,show
from mpl_toolkits.mplot3d import Axes3D

from utils.coordinate import Coordinate

class StrangeAttractor:
    """
    This is the lorentz attractor
    to simulate a chaotic trajectory
    """
    def __init__(self,time_step:float=1e-2) -> None:
        self.σ=10.
        self.ρ=28.
        self.β=8./3.
        self.dt = time_step
    
    def get_trajectory(self, initial_condition:Coordinate, steps:int) -> List[Coordinate]:
        coordinate = initial_condition
        for _ in range(steps):
            coordinate = self._get_next_coordinate(coordinate)
            yield coordinate

    def _get_next_coordinate(self, coordinate:Coordinate) -> Coordinate:
        return Coordinate(
            x=self._calculate_x(coordinate),
            y=self._calculate_y(coordinate),
            z=self._calculate_z(coordinate)
        )

    def _calculate_x(self,coordinate:Coordinate) -> float:
        x = coordinate.y - coordinate.x
        x *= self.σ
        x *= self.dt
        x += coordinate.x
        return x
    
    def _calculate_y(self,coordinate:Coordinate) -> float:
        y = self.ρ - coordinate.z
        y *= coordinate.x
        y -= coordinate.y
        y *= self.dt
        y += coordinate.y
        return y 

    def _calculate_z(self,coordinate:Coordinate) -> float:
        z = coordinate.x * coordinate.y
        z -= self.β * coordinate.z
        z *= self.dt 
        z += coordinate.z
        return z

    @staticmethod
    def display_trajectory(trajectory:List[Coordinate]) -> None:        
        xs = list(map(lambda coordinate:coordinate.x,trajectory))
        ys = list(map(lambda coordinate:coordinate.y,trajectory))
        zs = list(map(lambda coordinate:coordinate.z,trajectory))
        axis = figure().gca(projection = '3d')
        axis.scatter(xs, ys, zs, s=.5)
        show()