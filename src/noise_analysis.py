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
from triangulatepoints import triangulate_pairwise as tri_pw
import pandas as pd
from src.TrajectoryEstimation import interpolate_3d
import matplotlib.pyplot as plt

datamanager = DataManager()

# cam_swap_indices = [2, 3, 4, 5, 6, 7, 8, 9, 0, 1]
stds = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10]

data, constants, _ = datamanager.load('test_run')
proj_mat_all = datamanager.get_proj_mat_all()
# proj_mat_all[cam_swap_indices, :, :, :] = proj_mat_all
points_2d_all = datamanager.get_points_2d_all(set_oob_nan=True)
# points_2d_all[cam_swap_indices, :, :] = points_2d_all
oob_flags_all = datamanager.get_oob_flags_all()
# oob_flags_all[cam_swap_indices, :] = oob_flags_all

points_3d_gt = datamanager.get_points_3d()

amount_cam = constants['amount_of_cams']

metrics_nlr = np.zeros((len(stds), amount_cam - 1, 3))
metrics_pw = np.zeros((len(stds), amount_cam - 1, 3))
metrics_pw_med = np.zeros((len(stds), amount_cam - 1, 3))
for std_idx, std in enumerate(stds):
    print(f'Std: {std}')
    proj_mat_all_noise = datamanager.get_proj_mat_noise_all(intrinsic_std=0.00, extrinsic_std=0.00, seed=1)
    # proj_mat_all_noise[cam_swap_indices, :, :, :] = proj_mat_all_noise
    points_2d_noise_all = datamanager.get_points_2d_noise_all(set_oob_nan=True, std=std, seed=1)
    # points_2d_noise_all[cam_swap_indices, :, :] = points_2d_noise_all

    for num_cams in range(2, amount_cam+1):
        if num_cams == 2:
            points_3d_noise_nlr = tri_nlr(proj_mat_all_noise[0:num_cams, :, :, :],
                                          points_2d_noise_all[0:num_cams, :, :],
                                          oob_flags_all[0:num_cams, :], method='trf')
        else:
            points_3d_noise_nlr = tri_nlr(proj_mat_all_noise[0:num_cams, :, :, :],
                                          points_2d_noise_all[0:num_cams, :, :],
                                          oob_flags_all[0:num_cams, :])
        estimator_nlr = EstimationMetrics(points_3d_gt, points_3d_noise_nlr)
        metrics_nlr[std_idx, num_cams - 2, 0] = estimator_nlr.largest_difference()
        metrics_nlr[std_idx, num_cams - 2, 1] = estimator_nlr.euclidean_distance_sum()
        metrics_nlr[std_idx, num_cams - 2, 2] = estimator_nlr.root_mean_squared_error()

    print('NLR done')
    for num_cams in range(2, amount_cam+1):
        points_3d_pw = tri_pw(proj_mat_all_noise[0:num_cams, :, :, :],
                              points_2d_noise_all[0:num_cams, :, :], method='mean')
        estimator_pw = EstimationMetrics(points_3d_gt, points_3d_pw)
        metrics_pw[std_idx, num_cams - 2, 0] = estimator_pw.largest_difference()
        metrics_pw[std_idx, num_cams - 2, 1] = estimator_pw.euclidean_distance_sum()
        metrics_pw[std_idx, num_cams - 2, 2] = estimator_pw.root_mean_squared_error()
    print('Pairwise mean done')

    for num_cams in range(2, amount_cam+1):
        points_3d_pw_med = tri_pw(proj_mat_all_noise[0:num_cams, :, :, :],
                              points_2d_noise_all[0:num_cams, :, :], method='median')
        estimator_pw_med = EstimationMetrics(points_3d_gt, points_3d_pw_med)
        metrics_pw_med[std_idx, num_cams - 2, 0] = estimator_pw_med.largest_difference()
        metrics_pw_med[std_idx, num_cams - 2, 1] = estimator_pw_med.euclidean_distance_sum()
        metrics_pw_med[std_idx, num_cams - 2, 2] = estimator_pw_med.root_mean_squared_error()
    print('Pairwise median done')


plt.rcParams.update({'font.size': 7,
                     'figure.titlesize': 9,
                     'axes.labelsize': 7,
                     'axes.titlesize': 8,
                     'xtick.labelsize': 6,
                     'ytick.labelsize': 6,
                     'legend.fontsize': 6
                     })
fig, axs = plt.subplots(3, 1, figsize=[3.3, 6])
fig.suptitle('Impact of Noise vs. Multiple Cameras')
for i in range(0, amount_cam-1):
    axs[0].plot(stds, metrics_nlr[:, i, 2])

axs[0].set_ylim(0, np.nanmax(metrics_nlr[:, :, 2])*1.1)
axs[0].set_title('Nonlinear refinement')
axs[0].legend([f'{n} cameras' for n in range(2, amount_cam+1)])
axs[0].set(xlabel='standard deviation [px]', ylabel='root mean squared error [m]')

for i in range(0, amount_cam-1):
    axs[1].plot(stds, metrics_pw[:, i, 2])

axs[1].set_ylim(0, np.nanmax(metrics_pw[:, :, 2])*1.1)
axs[1].set_title('Pairwise averaging with mean')
axs[1].legend([f'{n} cameras' for n in range(2, amount_cam+1)])
axs[1].set(xlabel='standard deviation [px]', ylabel='root mean squared error [m]')

for i in range(0, amount_cam-1):
    axs[2].plot(stds, metrics_pw_med[:, i, 2])

axs[2].set_ylim(0, np.nanmax(metrics_pw_med[:, :, 2])*1.1)
axs[2].set_title('Pairwise averaging with median')
axs[2].legend([f'{n} cameras' for n in range(2, amount_cam+1)])
axs[2].set(xlabel='standard deviation [px]', ylabel='root mean squared error [m]')
fig.tight_layout()
plt.show()

visualizer = SoccerVisualizer()
visualizer.draw_ball_marker(points_3d_tv, size_marker=7, color='blue')
visualizer.draw_ball_marker(points_3d_noise_nlr, size_marker=7, color='red')
visualizer.draw_ball_marker(points_3d_gt, size_marker=7, color='lawngreen')
vispy.app.run()
print('The End.')