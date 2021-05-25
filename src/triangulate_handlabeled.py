import pandas as pd
import json
from pathlib import Path
import numpy as np

import vispy

from src.SoccerVisualizer import SoccerVisualizer
from triangulatepoints import triangulate_points_nonlinear_refinement

cwd = Path.cwd().parent
cam1_path = Path('hand_labeled/1015_1030/cam1/xy.csv')
cam7_path = Path('hand_labeled/1015_1030/cam7/xy.csv')
calib_path = Path('hand_labeled/calib.json')
cam_1 = pd.read_csv(cwd / cam1_path, names=['x', 'y'])[212:305]
cam_7 = pd.read_csv(cwd / cam7_path, names=['x', 'y']).fillna(-1)[212:305]

with open(cwd/calib_path) as f:
    calib = json.load(f)

K1 = np.array(calib['1']['K']).reshape(3, 3)
K7 = np.array(calib['7']['K']).reshape(3, 3)

R1 = np.array(calib['1']['R']).reshape(3, 3)
R7 = np.array(calib['7']['R']).reshape(3, 3)

T1 = np.array(calib['1']['T'])
T7 = np.array(calib['7']['T'])

proj_mat1 = np.hstack([K1 @ R1, T1.reshape(3, 1)])
proj_mat7 = np.hstack([K7 @ R7, T7.reshape(3, 1)])

num_points = len(cam_1)

proj_mat1s = np.repeat(proj_mat1[np.newaxis, :, :], num_points, axis=0)
proj_mat7s = np.repeat(proj_mat7[np.newaxis, :, :], num_points, axis=0)

proj_mats = np.stack([proj_mat1s, proj_mat7s], axis=0)

points_2d_all = np.stack([cam_1, cam_7], axis=0)

points_3d = triangulate_points_nonlinear_refinement(proj_mats, points_2d_all=points_2d_all)

print('Start Visualization')
visualizer = SoccerVisualizer()
visualizer.draw_ball_marker(points_3d, size_marker=7, color='lawngreen')

vispy.app.run()
# visualizer.draw_3d_line(points_3d+fi, color='red')

print('The End.')