from unittest import TestCase

import pandas.testing

from football.DataManager import DataManager
import numpy as np
from pathlib import Path
import pandas as pd



class TestDataManager(TestCase):

    @classmethod
    def setUpClass(self):
        self.mat_4 = np.array([1, 2, 3, 4])
        self.mat_3 = np.array([1, 2, 3])
        self.mat_2 = np.array([1, 2])
        self.mat_right = np.array([[0.3, 0.3, 0.3, 0],
                                   [0, 0.3, 0.3, 0],
                                   [0, 0, 1, 0]])

        self.frame = np.ones((100, 100, 3))

    def setUp(self):
        self.data_manager = DataManager()

        self.data_manager.set_extrinsic_mat(time=0, mat=self.mat_right, cam=0)
        self.data_manager.set_extrinsic_mat(time=0, mat=self.mat_right, cam=1)
        self.data_manager.set_intrinsic_mat(self.mat_right)
        self.data_manager.set_fov(30)
        self.data_manager.set_3d_ball_pos(time=0, pos=self.mat_3)
        self.data_manager.set_3d_ball_pos(time=1, pos=self.mat_3)
        self.data_manager.set_pix_ball_pos(time=0, pos=self.mat_2)
        self.data_manager.set_pix_ball_pos(time=1, pos=self.mat_2, cam=0)
        self.data_manager.set_pix_ball_pos(time=0, pos=self.mat_2, cam=1)
        self.data_manager.set_cam_node_orientation(time=0, orientation=self.mat_4)
        self.data_manager.set_cam_node_orientation(time=1, orientation=self.mat_4, cam=0)
        self.data_manager.set_cam_node_orientation(time=0, orientation=self.mat_4, cam=1)
        self.data_manager.set_cam_node_pos(time=0, pos=self.mat_3)
        self.data_manager.set_cam_node_pos(time=1, pos=self.mat_3, cam=0)
        self.data_manager.set_cam_node_pos(time=0, pos=self.mat_3, cam=1)
        self.data_manager.set_cam_orientation(time=0, orientation=self.mat_4)
        self.data_manager.set_cam_orientation(time=1, orientation=self.mat_4, cam=0)
        self.data_manager.set_cam_orientation(time=0, orientation=self.mat_4, cam=1)
        self.data_manager.set_frame(time=0, frame=self.frame, cam=0)
        self.data_manager.set_cam(time=2,
                                  extrinsic_mat=self.mat_right,
                                  cam_node_pos=self.mat_3,
                                  cam_node_orientation=self.mat_4,
                                  cam_orientation=self.mat_4,
                                  pix_ball_pos=self.mat_2,
                                  cam=0)

    def test_set_extrinsic_mat(self):
        np.testing.assert_array_equal(self.data_manager.data[0]['cam0_extrinsic_mat'], self.mat_right)
        np.testing.assert_array_equal(self.data_manager.data[0]['cam1_extrinsic_mat'], self.mat_right)

        with self.assertRaises(ValueError) as context:
            self.data_manager.set_extrinsic_mat(0, self.mat_3)

    def test_set_intrinsic_mat(self):
        np.testing.assert_array_equal(self.data_manager.constants['intrinsic_mat'], self.mat_right)

        with self.assertRaises(ValueError) as context:
            self.data_manager.set_intrinsic_mat(self.mat_3)

    def test_set_fov(self):

        self.assertTrue(self.data_manager.constants['fov'] == 30)

    def test_set_3d_ball_pos(self):

        np.testing.assert_array_equal(self.data_manager.data[0]['3d_ball_pos'], self.mat_3)

        np.testing.assert_array_equal(self.data_manager.data[1]['3d_ball_pos'], self.mat_3)

        with self.assertRaises(IndexError) as context:
            self.data_manager.set_3d_ball_pos(time=4, pos=self.mat_3)
        self.assertTrue('This time step does not exist yet. Please populate in order.' in str(context.exception))

    def test_set_pix_ball_pos(self):
        np.testing.assert_array_equal(self.data_manager.data[0]['cam0_pix_ball_pos'], self.mat_2)
        np.testing.assert_array_equal(self.data_manager.data[1]['cam0_pix_ball_pos'], self.mat_2)
        np.testing.assert_array_equal(self.data_manager.data[0]['cam1_pix_ball_pos'], self.mat_2)

        with self.assertRaises(IndexError) as context:
            self.data_manager.set_pix_ball_pos(time=4, pos=self.mat_2, cam=0)
        self.assertTrue('This time step does not exist yet. Please populate in order.' in str(context.exception))

    def test_set_cam_node_orientation(self):
        np.testing.assert_array_equal(self.data_manager.data[0]['cam0_node_orientation'], self.mat_4)

        np.testing.assert_array_equal(self.data_manager.data[1]['cam0_node_orientation'], self.mat_4)

        np.testing.assert_array_equal(self.data_manager.data[0]['cam1_node_orientation'], self.mat_4)

        with self.assertRaises(IndexError) as context:
            self.data_manager.set_cam_node_orientation(time=4, orientation=self.mat_4, cam=0)
        self.assertTrue('This time step does not exist yet. Please populate in order.' in str(context.exception))

    def test_set_cam_pos(self):
        np.testing.assert_array_equal(self.data_manager.data[0]['cam0_node_pos'], self.mat_3)

        np.testing.assert_array_equal(self.data_manager.data[1]['cam0_node_pos'], self.mat_3)

        np.testing.assert_array_equal(self.data_manager.data[0]['cam1_node_pos'], self.mat_3)

        with self.assertRaises(IndexError) as context:
            self.data_manager.set_cam_node_pos(time=4, pos=self.mat_4, cam=0)
        self.assertTrue('This time step does not exist yet. Please populate in order.' in str(context.exception))

    def test_set_cam_orientation(self):
        np.testing.assert_array_equal(self.data_manager.data[0]['cam0_orientation'], self.mat_4)
        np.testing.assert_array_equal(self.data_manager.data[1]['cam0_orientation'], self.mat_4)
        np.testing.assert_array_equal(self.data_manager.data[0]['cam1_orientation'], self.mat_4)

        with self.assertRaises(IndexError) as context:
            self.data_manager.set_cam_orientation(time=4, orientation=self.mat_4, cam=0)
        self.assertTrue('This time step does not exist yet. Please populate in order.' in str(context.exception))

    def test_set_frame(self):
        np.testing.assert_array_equal(self.data_manager.frames['cam0'][0], self.frame)
        with self.assertRaises(IndexError) as context:
            self.data_manager.set_frame(time=4, frame=self.frame, cam=0)
        self.assertTrue('Parameter time out of bounds. Please populate in order.' in str(context.exception))

    def test_set_cam(self):
        np.testing.assert_array_equal(self.data_manager.data[0]['cam0_extrinsic_mat'], self.mat_right)
        np.testing.assert_array_equal(self.data_manager.data[0]['cam0_orientation'], self.mat_4)
        np.testing.assert_array_equal(self.data_manager.data[0]['cam0_node_pos'], self.mat_3)
        np.testing.assert_array_equal(self.data_manager.data[0]['cam0_node_orientation'], self.mat_4)
        np.testing.assert_array_equal(self.data_manager.data[0]['cam0_pix_ball_pos'], self.mat_2)


    def test_write_data(self):
        self.data_manager.write_data('test_data.p')

        file = Path(Path.cwd().parent / 'football_data/test_data.p')
        self.assertTrue(file.is_file())

    def test_write_constants(self):
        self.data_manager.write_constants('test_constants.p')
        file = Path(Path.cwd().parent / 'football_data/test_constants.p')
        self.assertTrue(file.is_file())

    def test_load_data(self):
        self.data_manager.write_data('test_data.p')
        data_manager2 = DataManager()
        data_manager2.load_data('test_data.p')
        self.assertTrue(len(data_manager2.data) == len(self.data_manager.data))
        for x, y in zip(data_manager2.data, self.data_manager.data):
            self.assertTrue(x.keys() == y.keys())

    def test_load_constants(self):
        self.data_manager.write_constants('test_constants.p')
        data_manager2 = DataManager()
        data_manager2.load_constants('test_constants.p')
        self.assertTrue(data_manager2.constants.keys() == self.data_manager.constants.keys())

    def test_load_frame(self):
        self.data_manager.write_frame(time=7, cam=0, frame=self.frame, dirname='test')
        frame_new = self.data_manager.load_frame(7, 'test', 0)
        np.testing.assert_array_equal(frame_new, self.frame.astype('uint8'))

    def test_write_frames(self):
        self.data_manager.write_frames('test')
        for key in self.data_manager.frames:
            for i in range(len(self.data_manager.frames[key])):
                file = Path.cwd().parent / 'football_data/test' / (key + '_' + str(i).zfill(5) + '.png')
                self.assertTrue(file.is_file())

    def test_write_frame(self):
        self.data_manager.write_frame(time=7, cam=0, frame=self.frame, dirname='test')
        file = Path.cwd().parent / 'football_data/test' / 'cam0_00007.png'
        self.assertTrue(file.is_file())

if __name__ == '__main__':
    TestDataManager.run()
