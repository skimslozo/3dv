from scipy import interpolate
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from src.SoccerVisualizer import SoccerVisualizer


def interpolate_3d(points, steps):
    tck, u = interpolate.splprep(points, s=1/len(points))
    knots = interpolate.splev(tck[0], tck)
    u_fine = np.linspace(0,1,steps)
    points_fine = interpolate.splev(u_fine, tck)
    return points_fine


if __name__=='__main__':
    num_true_pts = 20
    s_true = np.linspace(0, 10, num_true_pts)
    x_true = np.cos(s_true)
    y_true = np.sin(s_true)
    z_true = s_true / 3

    points = np.asfarray([x_true, y_true, z_true])

    points_fine = interpolate_3d(points, 200)

    # fig = plt.figure()
    # ax3d = fig.add_subplot(111, projection='3d')
    # ax3d.plot(x_true, y_true, z_true, 'b*')
    # ax3d.plot(points_fine[0], points_fine[1], points_fine[2], 'g')
    # fig.show()
    # plt.show()

    visualizer = SoccerVisualizer()
    visualizer.draw_3d_line(points_fine, 'red')
    visualizer.draw_3d_line(points, 'blue')
    print('The End.')


