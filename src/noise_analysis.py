"""
Script to run the various triangulations and vispy visualizations
"""

import vispy
import numpy as np
from SoccerVisualizer import SoccerVisualizer
from EstimationMetrics import EstimationMetrics
from src.DataManager import DataManager
from triangulatepoints import triangulate_points_two_views as tri_tv
from triangulatepoints import triangulate_points_nonlinear_refinement as tri_nlr
import pandas as pd
from src.TrajectoryEstimation import interpolate_3d
import matplotlib.pyplot as plt

datamanager = DataManager()

cam_swap_indices = [2, 3, 4, 5, 6, 7, 8, 9, 0, 1]

data, constants = datamanager.load('run_mari')
proj_mat_all = datamanager.get_proj_mat_all()
# proj_mat_all[cam_swap_indices, :, :, :] = proj_mat_all
proj_mat_all_noise = datamanager.get_proj_mat_noise_all(intrinsic_std=0.00, extrinsic_std=0.01, seed=1724)
# proj_mat_all_noise[cam_swap_indices, :, :, :] = proj_mat_all_noise
points_2d_all = datamanager.get_points_2d_all(set_oob_nan=True)
# points_2d_all[cam_swap_indices, :, :] = points_2d_all
points_2d_noise_all = datamanager.get_points_2d_noise_all(set_oob_nan=True, std=10, seed=1724)
# points_2d_noise_all[cam_swap_indices, :, :] = points_2d_noise_all
oob_flags_all = datamanager.get_oob_flags_all()
# oob_flags_all[cam_swap_indices, :] = oob_flags_all

amount_cam = constants['amount_of_cams']

points_3d_gt = datamanager.get_points_3d()
points_3d_tv = tri_tv(proj_mat_all_noise[0], proj_mat_all_noise[1], points_2d_noise_all[0], points_2d_noise_all[1])
estimator_tv = EstimationMetrics(points_3d_gt, points_3d_tv)

metrics = np.zeros((amount_cam-1, 2))
for num_cams in range(2, amount_cam+1):
    points_3d_noise_nlr = tri_nlr(proj_mat_all_noise[0:num_cams, :, :, :],
                                  points_2d_noise_all[0:num_cams, :, :],
                                  oob_flags_all[0:num_cams, :])
    estimator_nlr = EstimationMetrics(points_3d_gt, points_3d_noise_nlr)
    metrics[num_cams-2, 0] = estimator_nlr.largest_difference()
    metrics[num_cams-2, 1] = estimator_nlr.euclidean_distance_sum()

metrics_df = pd.DataFrame(data=metrics, columns=['Largest Difference', 'Sum of Distances'])

largest_diff_tv = estimator_tv.largest_difference()
sum_diffs_tv = estimator_tv.euclidean_distance_sum()

fig, axs = plt.subplots(1, 2)
fig.suptitle('Impact of Noise vs. Multiple Cameras')
# plt.plot(range(2, 2+len(metrics_df)), metrics_df['Largest Difference'])
axs[0].plot(range(2, 2+len(metrics_df)), metrics_df['Sum of Distances'])
axs[0].plot([2, 1+len(metrics_df)], [sum_diffs_tv, sum_diffs_tv], '--')
axs[0].legend(['Sum of Distances', 'Two view reference'])
axs[0].set_title('Sum of Distances')
axs[0].set(xlabel='Number of Cameras', ylabel='Sum of Euclidean Distances')

axs[1].plot(range(2, 2+len(metrics_df)), metrics_df['Largest Difference'])
axs[1].plot([2, 1+len(metrics_df)], [largest_diff_tv, largest_diff_tv], '--')
axs[1].legend(['Largest Error', 'Two view reference'])
axs[1].set_title('Largest Error')
axs[1].set(xlabel='Number of Cameras', ylabel='Largest Error')
plt.show()

visualizer = SoccerVisualizer()
visualizer.draw_ball_marker(points_3d_tv, size_marker=7, color='blue')
visualizer.draw_ball_marker(points_3d_noise_nlr, size_marker=7, color='red')
visualizer.draw_ball_marker(points_3d_gt, size_marker=7, color='lawngreen')
vispy.app.run()
print('The End.')