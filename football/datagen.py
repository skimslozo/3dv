import numpy as np
import generate_dataset as gd

camera_positions = np.array([[-40, -140, 70],
                             [40, -140, 70],
                             [0, -140, 70]])
camera_rotations = np.array([[60, 0, 0],
                             [60, 0, 0],
                             [60, 0, 0]])
gd.generate_dataset('test_run', camera_positions, camera_rotations)

