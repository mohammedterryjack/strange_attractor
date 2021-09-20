from typing import List, Tuple

from sklearn.svm import SVC
from sklearn.exceptions import NotFittedError

from utils.coordinate import Coordinate
from utils.format_labels import (
    fill_labels, get_label_index_mappings,
    remove_consequtive_duplicates
)
from utils.plot_trajectory import display 

class StrangeAttractor:
    """
    This is the lorentz attractor
    to simulate a chaotic trajectory
    """
    def __init__(self) -> None:
        self.σ=10.
        self.ρ=28.
        self.β=8./3.
        self.dt = 1e-2
        
        self.minimum_steps_for_single_revolution = 80
        self.example_path_around_left_basin = list(
            self._simulate_trajectory(
                coordinate=Coordinate(-12.798100569892048,-13.682540178485027,31.779233776354452),
                steps=self.minimum_steps_for_single_revolution
            )
        )     
        self.example_path_around_right_basin = list(
            self._simulate_trajectory(
                coordinate= Coordinate(-4.858695591797552,7.301033219395926,35.09187885734113),
                steps=self.minimum_steps_for_single_revolution
            )
        )    

        self.classifier = SVC(decision_function_shape='ovr')
        self.index_label_mapping = {}
        self.label_index_mapping = {}
        
    def chaotic_trajectory_through_space(self,initial_condition:Tuple[float,float,float],steps:int,show_path:bool=False) -> List[str]:
        path = list(
            self._simulate_trajectory(
                coordinate=Coordinate(*initial_condition),
                steps=steps
            )
        )
        classes = self._tranform_coordinates_into_classes(path)
        if show_path:
            display(path,classes)
        return self._transform_classes_into_labels(classes)

    def _simulate_trajectory(self, coordinate:Coordinate, steps:int) -> List[Coordinate]:
        for _ in range(steps):
            coordinate = self._step(coordinate)
            yield coordinate

    def _step(self, coordinate:Coordinate) -> Coordinate:
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

    def fit_labels_to_attractor_space(self, leftspace_labels:List[str],rightspace_labels:List[str]) -> None:
        labels = list(self._get_labels(leftspace_labels)) + list(self._get_labels(rightspace_labels))
        self.index_label_mapping,self.label_index_mapping = get_label_index_mappings(labels)
        label_indexes = list(map(self.label_index_mapping.get,labels))
        self._train_classifier(label_indexes)

    def _train_classifier(self,label_indexes:List[int]) -> None:
        coordinates = self.example_path_around_left_basin + self.example_path_around_right_basin
        inputs = list(map(lambda coordinate:coordinate.as_tuple(),coordinates))
        self.classifier.fit(inputs, label_indexes)

    def _get_labels(self, pattern_labels:List[str]) -> List[str]:
        pattern_length = len(pattern_labels)
        assert 3 < pattern_length <= self.minimum_steps_for_single_revolution, "pattern provided was too small or too large to fit to the attractor space"
        return fill_labels(pattern_labels,self.minimum_steps_for_single_revolution//pattern_length)

    def _transform_classes_into_labels(self, class_indexes:List[int]) -> List[str]:
        return list(map(self.index_label_mapping.get,remove_consequtive_duplicates(class_indexes)))

    def _tranform_coordinates_into_classes(self,trajectory:List[Coordinate]) -> List[int]:
        inputs = list(map(lambda coordinate:coordinate.as_tuple(),trajectory))
        try:
            return self.classifier.predict(inputs)
        except NotFittedError:
            raise NotFittedError("first run fit_labels_to_attractor_space()")