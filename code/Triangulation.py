"""
Script to run the various triangulations and vispy visualizations
"""
import numpy as np
from SoccerVisualizer import SoccerVisualizer
from EstimationMetrics import EstimationMetrics
from football.DataManager import DataManager
from triangulatepoints import triangulate_points_two_views as tri_tv
from triangulatepoints import triangulate_points_nonlinear_refinement as tri_nlr
import vispy
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent / 'football'))


datamanager = DataManager()

data, constants = datamanager.load('test_run')
proj_mat_all = datamanager.get_proj_mat_all()
points_2d_all = datamanager.get_points_2d_all()

amount_cam = constants['amount_of_cams']

gt_points_3d = datamanager.get_points_3d()

points_3d_tv = tri_tv(proj_mat_all[0], proj_mat_all[2], points_2d_all[0], points_2d_all[2])
points_3d_nlr = tri_nlr(proj_mat_all, points_2d_all)

estimator_tv = EstimationMetrics(gt_points_3d, points_3d_tv)
estimator_nlr = EstimationMetrics(gt_points_3d, points_3d_nlr)

# print('The error of each estimated point: \n', estimator_tv.euclidean_distance())
print('The largest error for two views is: \n', estimator_tv.largest_difference())
print('The sum of errors for two views is: \n', estimator_tv.euclidean_distance_sum())
print('The largest error for {} views using Nonlinear Refinement is: \n'.format(amount_cam),
      estimator_nlr.largest_difference())
print('The sum of errors for {} views using Nonlinear Refinement is: \n'.format(amount_cam),
      estimator_nlr.euclidean_distance_sum())

visualizer = SoccerVisualizer()
visualizer.draw_ball_marker(points_3d_tv, size_marker=7, color='blue')
visualizer.draw_ball_marker(points_3d_nlr, size_marker=7, color='red')
visualizer.draw_ball_marker(gt_points_3d, size_marker=7, color='lawngreen')
vispy.app.run()
