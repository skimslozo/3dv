import numpy as np
import DatasetGenerator

camera_positions = np.array([[-40, -140, 70],
                             [40, -140, 70],
                             [0, -140, 70]])
camera_rotations = np.array([[60, 0, 0],
                             [60, 0, 0],
                             [60, 0, 0]])
dg = DatasetGenerator.DatasetGenerator()
dg.generate_dataset('test_run2', camera_positions, camera_rotations)

