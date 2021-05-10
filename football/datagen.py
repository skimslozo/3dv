import numpy as np
import DatasetGenerator

camera_positions = np.array([[ 0, -80, 60],
                             [-60, -140, 70],
                             [60, -140, 70],
                             [0, -140, 70],
                             [-60, 140, 70],
                             [60, 140, 70],
                             [0, 140, 70]])
camera_rotations = np.array([[50,0, 0],
                             [60, 0, -20],
                             [60, 0, 20],
                             [60, 0, 0],
                             [60, 0, -160],
                             [60, 0, 160],
                             [60, 0, 180]])
dg = DatasetGenerator.DatasetGenerator()
dg.generate_dataset('test', camera_positions, camera_rotations, steps=2000, save_frames=True, write_video=True, use_red_dot=False)

