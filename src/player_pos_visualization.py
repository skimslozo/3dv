
import matplotlib.pyplot as plt
import numpy as np

from src.DataManager import DataManager

def plot_points_on_image(img, points):
    fig = plt.figure(figsize=[14, 8])
    plt.imshow(frame)
    plt.scatter(points[:, 0], points[:, 1], c='red', s=20, alpha=0.3)
    plt.tight_layout()
    plt.show()
    # plt.close()


timestep = 0

datamanager = DataManager()
data, constants, dump = datamanager.load('test_run4')

player_poss = datamanager.get_2d_player_position(1)
# ball_poss2 = data_manager.get_points_2d(1)
frame = datamanager.load_frame(timestep, 'test_run4', 1)
# frame = frame[:, -1:0:-1, :] # mirror frame
#ball_poss[:, 0] = 1280 - ball_poss[:, 0] # offset x position
plot_points_on_image(frame, player_poss[0])
plt.close()

print('The End.')