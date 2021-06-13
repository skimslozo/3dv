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
# limitations under the License

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import logging
import glob

from gfootball.env import config
from gfootball.env import football_env
from gfootball.env import script_helpers
import numpy as np
from scipy.spatial.transform import Rotation as R
from numpy import array

from PIL import Image, ImageDraw

from DataManager import DataManager
from pathlib import Path


class DatasetGenerator():
    def __init__(self):
        pass

    def generate_dataset(self, run_name, cam_positions, cam_rotations, level='tests.11_vs_11_deterministic', steps=100,
                         render=True, save_frames=True,
                         write_video=False, use_red_dot=False, physics_steps_per_frame=10, amount_cam_follow=0,
                         render_resolution_x=1280, render_resolution_y=720, set_fov=24):
        """
        Automatically generate a data set for one game with multiple camera views

        Parameters
        ----------
        run_name :  name of the run, a directory with the data will be generated
        cam_positions : Nx3 array containing the positions of N different cameras
        cam_rotations: Nx3 array containing the rotation of N different cameras
        level: what deterministic scenario should be used. Options can be found in football/gfootball/scenarios/test .
        IMPORTANT: if you want to use a scenario that does not have the ending '_deterministic', open the scenario file
        and insure that the flag 'builder.config().deterministic' is set to True!
        render : if true the pygame window will appear and render the game (slower)
        save_frames : if true the frames of the game will be saved
        steps : amount of steps the simulation should make
        write_video : if true a video will be made from the frames, should only be true when save_frames is true
        use_red_dot: if True puts a red point in the frame where the ball is according to the pixel coordinates
        physics_steps_per_frame: 1 (Default). only tested with physics_steps_per_frame=1, higher values work but the
        2d pixel positions wont be perfect.
        amount_cam_follow: amount of cameras that should follow the ball, starting from the first.
        render_resolution_x: Height of the rendered frame
        render_resolution_y: Width of the rendered frame
        set_fov: Changes the field of view of all cameras

        Returns
        -------
        None.
        """
        if write_video:
            save_frames = True
        self.data_manager = DataManager()
        N = cam_positions.shape[0]
        if N < amount_cam_follow:
            print('amount_cam_follow to large, will be set to max')
            amount_cam_follow = N
        for i in range(N):
            if i < amount_cam_follow:
                cam_follow = True
            else:
                cam_follow = False

            self.generate_camera(run_name=run_name, cam_pos=cam_positions[i, :], cam_rot=cam_rotations[i, :], cam_nr=i,
                                 level=level, render=render, save_frames=save_frames, steps=steps,
                                 use_red_dot=use_red_dot, physics_steps_per_frame=physics_steps_per_frame,
                                 cam_follow=cam_follow, render_resolution_x=render_resolution_x,
                                 render_resolution_y=render_resolution_y, set_fov=set_fov)

        self.data_manager.write_data(run_name)
        self.data_manager.write_constants(run_name)


        run_path = Path.cwd().parent / 'football_data' / run_name
        dump_path = run_path/ '*.dump'
        dump_path_file = glob.glob(dump_path.as_posix())[0]
        script_helpers.ScriptHelpers().dump_to_txt(dump_path_file, run_path / (run_name +'_dump.txt'), False)


        print('END')

        if write_video:
            for cam in range(N):
                self.data_manager.write_video(run_name, cam)

    def procOut(self, cout, size):
        """
        Method for post-processing the lists output from the wrapper to numpy matrices

        Input:
          -cout: list (output from the wrapper) to-be processed, n x m
          -size [a, b]: a list- or tuple-like indiciating the desired shape of the output. a*b = n*m
          -use_red_dot: if True puts a red point in the frame where the ball is according to the pixel coordinates
        Output:
          - a x b np.matrix with reordered elements of cout in the desired format
        """
        size = (size[0], size[1])
        return np.matrix(np.reshape(np.array(cout), size))

    def generate_camera(self, run_name, cam_nr=0, steps=100, cam_pos=np.array([0, 0, 80]), cam_rot=np.array([0, 0, 0]),
                        level='tests.11_vs_11_deterministic', render=True, save_frames=False, use_red_dot=False,
                        physics_steps_per_frame=1, cam_follow=False, render_resolution_x=1280, render_resolution_y=720,
                        set_fov=24):

        players = ''
        dump_full_episodes = False
        tracesdir = '/tmp/dumps'
        if cam_nr == 0:
            dump_full_episodes = True
            tracesdir = Path.cwd().parent / 'football_data' / run_name
            tracesdir.mkdir(parents=True, exist_ok=True)

        assert not (any(['agent' in player for player in players])
                    ), ('Player type \'agent\' can not be used with play_game.')
        cfg = config.Config({
            'action_set': 'default',
            'dump_full_episodes': dump_full_episodes,
            'tracesdir': tracesdir,
            'players': players,
            'real_time': True,
            'game_engine_random_seed': 42,
            'level': level,
            'physics_steps_per_frame': physics_steps_per_frame,
            'render_resolution_x': render_resolution_x,
            'render_resolution_y': render_resolution_y
        })

        if physics_steps_per_frame != 10:
            config_update = {'real_time': False}
            cfg.update(config_update)

        # if level:
        #    cfg['level'] = level
        env = football_env.FootballEnv(cfg)
        print('Generating Cam {}:'.format(cam_nr))
        if render:
            env.render()
        env.reset()

        pos = 0
        try:
            for time in range(steps):
                print('Progress: ', round((time/steps)*100), '%')
                r = R.from_euler('xyz', cam_rot, degrees=True)
                carot_quat = r.as_quat()
                pos += 0.1
                env._env._env.set_camera_node_orientation(-0.0, -0.0, -0.0, 1.0)

                if (cam_follow):
                    ball3d = self.procOut(cout=env._env._env.get_3d_ball_position(), size=[3, 1])
                    env._env._env.set_camera_node_position(float(cam_pos[0] + ball3d[0]), float(cam_pos[1] + ball3d[1]),
                                                           float(cam_pos[2] + ball3d[2]))
                else:
                    env._env._env.set_camera_node_position(float(cam_pos[0]), float(cam_pos[1]), float(cam_pos[2]))

                env._env._env.set_camera_orientation(carot_quat[0], carot_quat[1], carot_quat[2], carot_quat[3])
                env._env._env.set_camera_fov(set_fov)

                _, _, done, _ = env.step([])

                RT0 = self.procOut(cout=env._env._env.get_extrinsics_matrix(), size=[3, 4])
                K0 = self.procOut(cout=env._env._env.get_intrinsics_matrix(), size=[3, 3])
                ball3d = self.procOut(cout=env._env._env.get_3d_ball_position(), size=[3, 1])
                camPos0 = self.procOut(cout=env._env._env.get_camera_node_position(), size=[3, 1])
                camOr0 = self.procOut(cout=env._env._env.get_camera_orientation(), size=[1, 4])
                CNO0 = self.procOut(cout=env._env._env.get_camera_node_orientation(), size=[1, 4])
                fov = env._env._env.get_camera_fov()
                pixcoord0 = self.procOut(cout=env._env._env.get_pixel_coordinates(), size=[2, 1])
                oob_flag = env._env._env.is_ball_OOB()  # out of bounds flag

                # print("CNO: ", env._env._env.get_camera_node_orientation())
                # print("CNP1: ", env._env._env.get_camera_node_position())
                # print("CO: ", env._env._env.get_camera_orientation())
                # print("CFOV: ", env._env._env.get_camera_fov())
                # print('RT', RT)
                # print("PIX2D 1: ", env._env._env.get_pixel_coordinates())
                # print('Ball 3D: ', ball3d)
                # print('----------------------------')
                if cam_nr == 0:
                    self.data_manager.set_fov(fov)
                    self.data_manager.set_intrinsic_mat(K0)
                    self.data_manager.set_3d_ball_pos(time=time, pos=ball3d)
                self.data_manager.set_cam(time=time,
                                          extrinsic_mat=RT0,
                                          cam_node_pos=camPos0,
                                          cam_node_orientation=CNO0,
                                          pix_ball_pos=pixcoord0,
                                          cam_orientation=camOr0,
                                          oob_flag=oob_flag,
                                          cam=cam_nr)
                if save_frames:
                    _frame = env.observation()['frame']
                    if use_red_dot:
                        img = Image.fromarray(_frame.astype('uint8'))
                        draw = ImageDraw.Draw(img)
                        r = 5
                        x = pixcoord0[0]
                        y = pixcoord0[1]
                        leftUpPoint = (x - r, y - r)
                        rightDownPoint = (x + r, y + r)
                        twoPointList = [leftUpPoint, rightDownPoint]
                        draw.ellipse(twoPointList, fill=(255, 0, 0, 255))
                        _frame = np.array(img)
                    self.data_manager.write_frame(time=time, frame=_frame, cam=cam_nr, run_name=run_name)

                time += 1

                if done:
                    '''
                    if cam_nr == 0:
                        dump_name = 'datagen_' + run_name  # DO NOT CHANGE THIS 'datagen' MUST be the first 7 letters
                        env.write_dump(dump_name)
                    '''
                    env.reset()
            # end for


        except KeyboardInterrupt:
            logging.warning('Game stopped, writing dump...')

            exit(1)
