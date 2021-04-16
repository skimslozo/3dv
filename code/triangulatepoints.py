import numpy as np
import cv2

def triangulatePoints_twoviews(projmat0, projmat1, points_2d_0, points_2d_1):
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
    N = points_2d_0.shape[0]
    points_3d = np.zeros((N, 3))

    for frame_nr in range(N):
        point_3d = cv2.triangulatePoints(projmat0[frame_nr], projmat1[frame_nr], points_2d_0[frame_nr], points_2d_1[frame_nr])
        point_3d /= point_3d[3]
        points_3d[frame_nr, :] = point_3d[:3].reshape((1, -1))

    return points_3d