import numpy as np
from SoccerVisualizer import SoccerVisualizer
from EstimationMetrics import EstimationMetrics
from football.DataManager import DataManager
from triangulatepoints import triangulatePoints_twoviews
import vispy

datamanager = DataManager()
data = datamanager.load_data('run1_data.p')
constants = datamanager.load_constants('run1_constants.p')

k_0 = np.array(constants['intrinsic_mat'])
points_2d_0 = datamanager.get_points_2d(0)
points_2d_1 = datamanager.get_points_2d(1)
ext_mat_0 = datamanager.get_ext_mat(0)
ext_mat_1 = datamanager.get_ext_mat(1)
gt_points_3d = datamanager.get_points_3d()

proj_mat_0 = k_0 @ ext_mat_0
proj_mat_1 = k_0 @ ext_mat_1

points_3d = triangulatePoints_twoviews(proj_mat_0, proj_mat_1, points_2d_0, points_2d_1)

estimator = EstimationMetrics(gt_points_3d, points_3d)
print('The error of each estimated point: \n', estimator.euclidean_distance())
print('The largest error is: \n', estimator.largest_difference())

visualizer = SoccerVisualizer()
visualizer.draw_ball_marker(points_3d, size_marker=7, color='red')
visualizer.draw_ball_marker(gt_points_3d, size_marker=7, color='lawngreen')
vispy.app.run()
