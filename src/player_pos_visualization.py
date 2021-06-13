
import matplotlib.pyplot as plt
import numpy as np

from src.DataManager import DataManager

def plot_points_on_image(img, points):
    fig = plt.figure(figsize=[14, 8])
    plt.imshow(frame)
    plt.scatter(points[:, 0], points[:, 1], c='red', s=20, alpha=1)
    plt.tight_layout()
    plt.axis('off')
    # plt.show()
    # plt.close()

datamanager = DataManager()
data, constants, dump = datamanager.load('test_run2')

timestep = 0

player_poss = datamanager.get_2d_player_position(1)
# ball_poss2 = data_manager.get_points_2d(1)
for i in range(player_poss.shape[0]):
    frame = datamanager.load_frame(i, 'test_run2', 1)
    # frame = frame[:, -1:0:-1, :] # mirror frame
    #ball_poss[:, 0] = 1280 - ball_poss[:, 0] # offset x position
    plot_points_on_image(frame, player_poss[i])
    plt.savefig("player_images/" + str(i).zfill(4) + ".png", bbox_inches='tight')
    plt.close()

print('The End.')