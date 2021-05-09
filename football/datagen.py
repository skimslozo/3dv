import numpy as np
import DatasetGenerator

camera_positions = np.array([[-60, -140, 70],
                             [60, -140, 70],
                             [0, -140, 70],
                             [-60, 140, 70],
                             [60, 140, 70],
                             [0, 140, 70]])
camera_rotations = np.array([[60, 0, -20],
                             [60, 0, 20],
                             [60, 0, 0],
                             [60, 0, -160],
                             [60, 0, 160],
                             [60, 0, 180]])
dg = DatasetGenerator.DatasetGenerator()
dg.generate_dataset('test_run', camera_positions, camera_rotations, steps=50, save_frames=False, write_video=False)

