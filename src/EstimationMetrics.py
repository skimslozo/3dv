import numpy as np


class EstimationMetrics:
    def __init__(self, gt_points_3d, points_3d):
        self.gt_points_3d = gt_points_3d
        self.points_3d = points_3d
        if gt_points_3d.shape != points_3d.shape:
            raise ValueError('Ground Truth and Input size miss match')

    def set_points(self, points_3d):
        if self.gt_points_3d.shape != points_3d.shape:
            raise ValueError('Ground Truth and Input size miss match')
        self.points_3d = points_3d

    def euclidean_distance(self):
        return np.linalg.norm(self.gt_points_3d - self.points_3d, axis=1)

    def root_mean_squared_error(self):
        return self.euclidean_distance_sum()/len(self.points_3d)

    def euclidean_distance_sum(self):
        return np.sum(self.euclidean_distance())

    def largest_difference(self):
        return np.max(self.euclidean_distance())


if __name__ == '__main__':
    gt_test = np.array(range(15)).reshape((-1, 3))
    test = gt_test * 2
    estimator = EstimationMetrics(gt_points_3d=gt_test, points_3d=test)
    eucdist_test = estimator.euclidean_distance()
    print(eucdist_test)
    max_error_test = estimator.largest_difference()
    print(max_error_test)
