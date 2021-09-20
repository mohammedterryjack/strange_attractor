from typing import Tuple 

class Coordinate:
    def __init__(self,x:float,y:float,z:float) -> None:
        self.x= x
        self.y= y
        self.z= z
    
    def as_tuple(self) -> Tuple[float,float,float]:
        return (self.x,self.y,self.z)

    def __repr__(self) -> str:
        return str(self.as_tuple())