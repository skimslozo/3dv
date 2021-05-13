import numpy as np
import DatasetGenerator
import DataManager





camera_positions = np.array([[ 0, -80, 60],
                             [-60, -140, 70],
                             [60, -140, 70],
                             [0, -140, 70],
                             [-60, 140, 70],
                             [60, 140, 70],
                             [0, 140, 70,],
                             [0, 0, 80],])
camera_rotations = np.array([[50,0, 0],
                             [60, 0, -20],
                             [60, 0, 20],
                             [60, 0, 0],
                             [60, 0, -160],
                             [60, 0, 160],
                             [60, 0, 180],
                             [0, 0, 180],
                             ])
dg = DatasetGenerator.DatasetGenerator()
dg.generate_dataset('othergroup', camera_positions, camera_rotations, steps=200, save_frames=True, write_video=True, use_red_dot=False)

a = DataManager.DataManager()
a.write_csv_proj('othergroup')





