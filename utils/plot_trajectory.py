from typing import List, Optional

from matplotlib.pyplot import figure,show
from mpl_toolkits.mplot3d import Axes3D

from utils.coordinate import Coordinate
    
def display(coordinates:List[Coordinate], classes:Optional[List[int]]=None) -> None:        
    xs = list(map(lambda coordinate:coordinate.x,coordinates))
    ys = list(map(lambda coordinate:coordinate.y,coordinates))
    zs = list(map(lambda coordinate:coordinate.z,coordinates))
    colours = [0]*len(coordinates) if classes is None else classes

    axis = figure().gca(projection = '3d')
    axis.scatter(xs, ys, zs, c=colours, s=.5)
    show()