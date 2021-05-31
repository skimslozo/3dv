import numpy as np
import cv2
from scipy.optimize import least_squares


def triangulate_points_two_views(projmat0, projmat1, points_2d_0, points_2d_1):
    """
    cv2.triangulatePoints wrapper to allow for changing projection matricies
    Args:
        projmat0: N long Array of 3x4 arrays containing the projection matrix ( K* [RT]) for each frame for camera 0
        projmat1: N long Array of 3x4 arrays containing the projection matrix ( K* [RT]) for each frame for camera 1
        points_2d_0: Nx2 array containing the pixel coordinates of the point for camera 0
        points_2d_1: Nx2 array containing the pixel coordinates of the point for camera 1

    Returns:
        points_3d: Nx3 array containing the 3d world coordinates of points
    """
    steps = points_2d_0.shape[0]
    points_3d = np.zeros((steps, 3))

    for frame_nr in range(steps):
        point_3d = cv2.triangulatePoints(projmat0[frame_nr], projmat1[frame_nr], points_2d_0[frame_nr],
                                         points_2d_1[frame_nr])
        point_3d /= point_3d[3]
        points_3d[frame_nr, :] = point_3d[:3].reshape((1, -1))

    return points_3d


def project(projmat, point_3d):
    point_3d = np.concatenate((point_3d, np.array([1])))
    point_2d = projmat @ point_3d
    point_2d /= point_2d[2]
    return point_2d[:2]


def tri_residual(point_3d, **kwargs):
    proj_mat_all = kwargs['proj_mat_all']
    point_2d_all = kwargs['point_2d_all']
    amount_cam = kwargs['amount_cam']
    residual = np.zeros(amount_cam)
    for cam in range(amount_cam):
        residual[cam] = np.linalg.norm(point_2d_all[cam] - project(proj_mat_all[cam], point_3d))
    return residual


def triangulate_points_nonlinear_refinement(proj_mat_all, points_2d_all, oob_flags_all, method='lm'):
    """
    Triangulates the real world position of a point in world coordinates in N time steps based on M views \
    using the Nonlinear Refinement technique.

    @param proj_mat_all: M X N X 3 X 4 array, containing projection Matrices where M is the number of cameras \
    and N is the amount of steps.
    @param points_2d_all: M X N X 2 array, containing the position of the ball in pixel coordinates for each \
    frame n and each camera m.
    @param oob_flags_all: M X N array, containing the out of bounds flags for each frame n and each camera m.
    @param method: method to be used by the least_squares function, default is 'lm', but this method only works for 3
    or more cameras, if there are only two cameras the method ‘trf’ should be used.
    @return: 3d_points, triangulated 3d position of the ball
    """
    shape = proj_mat_all.shape
    amount_cam = shape[0]
    steps = shape[1]

    if amount_cam == 2 and method == 'lm':
        print('Warning: Only two camera views where given but method was set to \'lm\' which needs at least three'
              ' views. Method was changed to \'trf\'.')
        method = 'trf'
    assert amount_cam >= 2, 'Not enough cameras to triangulate, only {} cameras'.format(amount_cam)

    initial_guess_3d = np.zeros((3, 1)).flatten()
    points_3d = np.zeros((steps, 3))
    for step in range(steps):
        cur_oob_flags = oob_flags_all[:, step]
        cur_proj_mat_all = proj_mat_all[~cur_oob_flags, step, :, :]
        cur_points_2d_all = points_2d_all[~cur_oob_flags, step, :]

        cur_amount_cam = cur_points_2d_all.shape[0]
        if cur_amount_cam == 2 and method == 'lm':
            print('Warning: Only two camera views where given but method was set to \'lm\' which needs at least three'
                  ' views. Method was changed to \'trf\'.')
            cur_method = 'trf'
        else:
            cur_method = method
        assert cur_amount_cam >= 2, 'Not enough cameras to triangulate, only {amount} cameras in step {cur_step}'.format(
            amount=cur_amount_cam, cur_step=step)

        ls = least_squares(tri_residual, initial_guess_3d, method=cur_method, max_nfev=10000, kwargs={'proj_mat_all': cur_proj_mat_all,
                                                                                'point_2d_all': cur_points_2d_all,
                                                                                'amount_cam': cur_amount_cam}) # loss = 'cauchy'
        points_3d[step] = ls.x

    return points_3d
