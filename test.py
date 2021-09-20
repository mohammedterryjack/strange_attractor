from src.strange_attractor import StrangeAttractor

chaos = StrangeAttractor()
chaos.fit_labels_to_attractor_space(
   leftspace_labels=[1,2,3,4,5,6,7,8,9,10],
   rightspace_labels=[-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]
)
labels = chaos.chaotic_trajectory_through_space(
    initial_condition=(1.0,-0.2,.3),
    steps=1000,
    show_path=True
)
print(labels)