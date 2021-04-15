import numpy as np
import pandas as pd
from SoccerVisualizer import SoccerVisualizer
import cv2
import vispy
from pathlib import Path

data_path = Path(Path.cwd().parent / 'football_data')
df_data = pd.read_json(Path(data_path / 'run1_data.json'))
df_constants = pd.read_json(Path(data_path / 'run1_constants.json'))

k_1 = np.array(df_constants['intrinsic_mat'][0])
pix_ball_pos_cam0_all = df_data['pix_ball_pos_cam0']
pix_ball_pos_cam1_all = df_data['pix_ball_pos_cam1']
extrinsic_mat_cam0_all = df_data['extrinsic_mat_cam0']
extrinsic_mat_cam1_all = df_data['extrinsic_mat_cam1']
points_3d = np.zeros((df_data.shape[0], 3))

for i in range(df_data.shape[0]):
    pix_ball_pos_cam0 = np.array(pix_ball_pos_cam0_all[i])
    pix_ball_pos_cam1 = np.array(pix_ball_pos_cam1_all[i])
    extrinsic_mat_cam0 = np.array(extrinsic_mat_cam0_all[i])
    extrinsic_mat_cam1 = np.array(extrinsic_mat_cam1_all[i])
    T_0 = k_1 @ extrinsic_mat_cam0
    T_1 = k_1 @ extrinsic_mat_cam1
    point_3d = cv2.triangulatePoints(T_0, T_1, pix_ball_pos_cam0, pix_ball_pos_cam1)
    point_3d /= point_3d[3]
    points_3d[i, :] = point_3d[:3].reshape((1, -1))


visualizer = SoccerVisualizer()

ball_pos = points_3d

visualizer.draw_ball(ball_pos)
vispy.app.run()
