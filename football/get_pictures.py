# coding=utf-8
# Copyright 2019 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Script allowing to play the game by multiple players.

Use this demo launcher to extract useful info from the simulation directly, real-time. 

Handy functions:

      - set_camera_node_orientation(x, y, z, w, cam) - set the orientation of cam (cam = 1 or 2), input in quaternions
      - set_camera_node_position(x, y, z, cam) - set the cam poisition. 
      - set_camera_orientation(x, y, z, w, cam) - set the camera node position. My best guess is that it allows to decouple the viewpoint coordinates from the camera coordinate sysetm
      - set_camera_fov(24, cam) - set the (half!) horizontal field of view value
      - get_extrinsics_matrix(cam) - returns the rigid-body transformation matrix from the world coordinates to the camera coordinates
      - get_intrinsics_matrix(cam) - returns the calibration matrix of the camera
      - get_3d_ball_position() - returns the 3d ground-truth position of the ball
      - get_camera_node_position(cam) - returns the camera node position in the world coordinate frame
      - get_camera_orientation(cam) - returns the camera orientation w.r.t to the world coordinate frame
      - get_camera_fov(cam) - returns camera fov
      - get_pixel_coordinates(cam) - returns 2d pixel coordinates of the ball in cam
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
from absl import logging


from gfootball.env import config
from gfootball.env import football_env
import numpy as np
from scipy.spatial.transform import Rotation as R

from football.DataManager import DataManager

FLAGS = flags.FLAGS

flags.DEFINE_string('players', 'keyboard:left_players=1',
                    'Semicolon separated list of players, single keyboard '
                    'player on the left by default')
flags.DEFINE_string('level', '', 'Level to play')
flags.DEFINE_enum('action_set', 'default', ['default', 'full'], 'Action set')
flags.DEFINE_bool('real_time', True,
                  'If true, environment will slow down so humans can play.')
flags.DEFINE_bool('render', True, 'Whether to do game rendering.')


def procOut(cout, size):
  """Method for post-processing the lists output from the wrapper to numpy matrices
  
  Input: 
    -cout: list (output from the wrapper) to-be processed, n x m
    -size [a, b]: a list- or tuple-like indiciating the desired shape of the output. a*b = n*m
    
  Output:
    - a x b np.matrix with reordered elemetns of cout in the desired format"""
  size = (size[0], size[1])
  return np.matrix(np.reshape(np.array(cout), size))

def main(_):
  players = FLAGS.players.split(';') if FLAGS.players else ''
  assert not (any(['agent' in player for player in players])
             ), ('Player type \'agent\' can not be used with play_game.')
  cfg = config.Config({
      'action_set': FLAGS.action_set,
      'dump_full_episodes': True,
      'players': players,
      'real_time': FLAGS.real_time,
  })
  if FLAGS.level:
    cfg['level'] = FLAGS.level
  env = football_env.FootballEnv(cfg)
  print('hi')
  if FLAGS.render:
    env.render()
  env.reset()

  camrot = np.array([60, 0, 0]) # handy to set the camera coordinates in Euler angles

  data_manager = DataManager()

  try:
    for time in range(10):
      r = R.from_euler('xyz', camrot, degrees = True)
      carot_quat = r.as_quat()

      # The second camera is hard-coded, so it does not scale to multiple cameras yet. Additionally, if you only use one camera with custom positions,
      # The second once won't really work. Point being - if you use both cameras, explicitly define all custom parameters for both cameras.
      
      env._env._env.set_camera_node_orientation(-0.0, -0.0, -0.0, 1.0, 1)
      env._env._env.set_camera_node_position(-40, -140, 70, 1)
      env._env._env.set_camera_orientation(carot_quat[0], carot_quat[1], carot_quat[2], carot_quat[3], 1)
      env._env._env.set_camera_fov(24, 1)

      env._env._env.set_camera_node_orientation(-0.0, -0.0, -0.0, 1.0, 2)
      env._env._env.set_camera_node_position(40, -140, 70, 2)
      env._env._env.set_camera_orientation(carot_quat[0], carot_quat[1], carot_quat[2], carot_quat[3], 2)
      env._env._env.set_camera_fov(24, 2)

      _, _, done, _ = env.step([])     

      RT0 = procOut(env._env._env.get_extrinsics_matrix(1), [3, 4])
      RT1 = procOut(env._env._env.get_extrinsics_matrix(2), [3, 4])
      K0 = procOut(env._env._env.get_intrinsics_matrix(1), [3, 3])
      K1 = procOut(env._env._env.get_intrinsics_matrix(2), [3, 3])
      ball3d = procOut(env._env._env.get_3d_ball_position(), [3, 1])
      ball3dh = np.transpose(np.matrix(np.append(np.array(ball3d), 1)))
      camPos0 = procOut(env._env._env.get_camera_node_position(1), [3, 1])
      camPos1 = procOut(env._env._env.get_camera_node_position(2), [3, 1])
      camOr0 = procOut(env._env._env.get_camera_orientation(1), [1, 4])
      camOr1 = procOut(env._env._env.get_camera_orientation(2), [1, 4])
      fov = env._env._env.get_camera_fov(1)
      pixcoord0 = procOut(env._env._env.get_pixel_coordinates(1), [2, 1])
      pixcoord1 = procOut(env._env._env.get_pixel_coordinates(2), [2, 1])
      CNO0 = env._env._env.get_camera_node_orientation(1)
      CNO1 = env._env._env.get_camera_node_orientation(2)

      # print("CNO: ", env._env._env.get_camera_node_orientation(1))
      # print("CNP1: ", env._env._env.get_camera_node_position(1))
      # print("CNP2: ", env._env._env.get_camera_node_position(2))
      # print("CO: ", env._env._env.get_camera_orientation(1))
      # print("CFOV: ", env._env._env.get_camera_fov(1))
      # print('RT', RT)
      # print("PIX2D 1: ", env._env._env.get_pixel_coordinates(1))
      # print("PIX2D 2: ", env._env._env.get_pixel_coordinates(2))
      # print('Ball 3D: ', ball3d)
      # print('----------------------------')
      data_manager.set_fov(fov)
      data_manager.set_intrinsic_mat(K0)
      data_manager.set_3d_ball_pos(time=time, pos=ball3d)
      data_manager.set_cam(time=time, cam_node_pos=camPos0, cam_node_orientation=CNO0, pix_ball_pos=pixcoord0,
                           cam_orientation=camOr0, cam=0)
      data_manager.set_extrinsic_mat(time=time, mat=RT0, cam=0)
      data_manager.set_extrinsic_mat(time=time, mat=RT1, cam=1)
      data_manager.set_cam(time=time, cam_node_pos=camPos1, cam_node_orientation=CNO0, pix_ball_pos=pixcoord1,
                           cam_orientation=camOr1, cam=1)


      time += 1

      if done:
        env.reset()

    # end for
    data_manager.write_data('run1_data.p')
    data_manager.write_constants('run1_constants.p')

  except KeyboardInterrupt:
    logging.warning('Game stopped, writing dump...')
    env.write_dump('shutdown')
    exit(1)


if __name__ == '__main__':
  app.run(main)
