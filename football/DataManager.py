import os
from pathlib import Path

import numpy as np
import pandas as pd

class DataManager:

    def __init__(self):
        self.constants = {} # dict
        self.data = [{}] # list of dicts
        self.frames = [{}]

    def set_extrinsic_mat(self, time: int, mat: np.ndarray, cam=0):
        if mat.shape != (3, 4) and mat.shape != (4, 4):
            raise ValueError('Wrong Dimension. Extrinsic matrix has dimension 3x4')
        self._check_time(time)
        self.data[time]['extrinsic_mat_cam' + str(cam)] = mat

    def set_intrinsic_mat(self, mat: np.ndarray):
        if mat.shape != (3, 3) and mat.shape!= (3, 4):
            raise ValueError('Wrong Dimension. Extrinsic matrix has dimension 3x3')
        self.constants['intrinsic_mat'] = mat

    def set_fov(self, fov: float):
        self.constants['fov'] = fov

    def set_3d_ball_pos(self, time, pos):
        self._check_time(time)
        self.data[time]['3d_ball_pos'] = pos

    def _check_time(self, time):
        if len(self.data) == time:
            self.data.append({})
        if len(self.data) < time:
            raise IndexError('This time step does not exist yet. Please populate in order.')

    def set_pix_ball_pos(self, time, pos, cam=0):
        self._check_time(time)
        self.data[time]['pix_ball_pos_cam' + str(cam)] = pos

    def set_cam_node_orientation(self, time, orientation, cam=0):
        self._check_time(time)
        self.data[time]['cam' + str(cam) + '_node_orientation'] = orientation

    def set_cam_node_pos(self, time, pos, cam=0):
        self._check_time(time)
        self.data[time]['cam' + str(cam) + '_node_pos'] = pos

    def set_cam_orientation(self, time, orientation, cam=0):
        self._check_time(time)
        self.data[time]['cam' + str(cam) + '_orientation'] = orientation

    def set_frame(self, time, frame, cam):
        self._check_time(time)
        self.frames[time]['cam'+ str(cam)] = frame

    def set_cam(self, time, cam_node_pos, cam_node_orientation, cam_orientation, pix_ball_pos, cam):
        self.set_cam_node_pos(time, cam_node_pos, cam)
        self.set_cam_node_orientation(time, cam_node_orientation, cam)
        self.set_cam_orientation(time, cam_orientation, cam)
        self.set_pix_ball_pos(time, pix_ball_pos, cam)

    def write_data_to_json(self, filename):
        Path(Path.cwd().parent / 'football_data').mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(self.data)
        df.index.rename('time', inplace=True)
        df.to_json(Path.cwd().parent / 'football_data/' / filename, index=True)
        return df

    def write_constants_to_json(self, filename):
        Path(Path.cwd().parent / 'football_data').mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame([self.constants])
        df.to_json(Path.cwd().parent / 'football_data' / filename, index=True)
        return df

    def load_data_from_json(self, filename):
        path = Path.cwd().parent / 'football_data' / filename
        df = pd.read_json(path)
        self.data = df.T.to_dict()
        return df

    def load_constants_from_json(self, filename):
        path = Path.cwd().parent / 'football_data' / filename
        df = pd.read_json(path)
        self.constants = df.loc[0].to_dict()
        return df









