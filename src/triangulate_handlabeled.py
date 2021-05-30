import pandas as pd
import json
from pathlib import Path
import numpy as np

import vispy

import numpy as np


import threading

import time

from SoccerVisualizer import SoccerVisualizer
from triangulatepoints import triangulate_points_two_views

cwd = Path.cwd().parent
cam1_path = Path('hand_labeled/1015_1030/cam1/xy.csv')
cam7_path = Path('hand_labeled/1015_1030/cam7/xy.csv')
calib_path = Path('hand_labeled/calib.json')
cam_1 = pd.read_csv(cwd / cam1_path, names=['x', 'y'])[250:550]
cam_7 = pd.read_csv(cwd / cam7_path, names=['x', 'y']).fillna(-1)[250:550]

with open(cwd/calib_path) as f:
    calib = json.load(f)

K1 = np.array(calib['1']['K']).reshape(3, 3)
K7 = np.array(calib['7']['K']).reshape(3, 3)

R1 = np.array(calib['1']['R']).reshape(3, 3)
R7 = np.array(calib['7']['R']).reshape(3, 3)

T1 = np.array(calib['1']['T']).reshape(3, 1)
T7 = np.array(calib['7']['T']).reshape(3, 1)

proj_mat1 = K1 @ np.hstack([R1, T1])
proj_mat7 = K7 @ np.hstack([R7, T7])

num_points = len(cam_1)

proj_mat1s = np.repeat(proj_mat1[np.newaxis, :, :], num_points, axis=0)
proj_mat7s = np.repeat(proj_mat7[np.newaxis, :, :], num_points, axis=0)

proj_mats = np.stack([proj_mat1s, proj_mat7s], axis=0)

points_2d_all = np.stack([cam_1, cam_7], axis=0)

points_3d = triangulate_points_two_views(proj_mat1s, proj_mat7s,  cam_1.values, cam_7.values)

print('Start Visualization')
visualizer = SoccerVisualizer()
visualizer.draw_ball_marker(points_3d, size_marker=7, color='lawngreen', timer=True)





visualizer._timer.start(0.1)
vispy.app.run()

# visualizer.draw_3d_line(points_3d+fi, color='red')

print('The End.')