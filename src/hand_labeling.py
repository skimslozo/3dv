import cv2
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt

from pathlib import Path

import csv

import numpy as np
import numpy as np

def nan_helper(y):
    """ copied from https://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array
    
    Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]

def create_frames():
    video_path = Path.cwd().parent / 'football_data' / 'EPTS - Camera 7.mp4'
    vidcap = cv2.VideoCapture(str(video_path))
    success,image = vidcap.read()


    count = 0
    path_folder = Path.cwd().parent / 'football_data' / 'hand_labeled' / '1015_1030' / 'cam7'
    path_folder.mkdir(parents=True, exist_ok=False)

    while success:
        path = path_folder / ('frame' + str(count) + '.jpg')
        print(path)
        cv2.imwrite(str(path), image)     # save frame as JPEG file      
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1



def create_xy_file():

    path_folder = Path.cwd().parent / 'football_data' / 'hand_labeled' / '1015_1030' / 'cam7'
    data_points = []
    for i in range(801):

        path_file = path_folder / ('frame' + str(i) + '.xml')

        if path_file.is_file():

            # assume PacalVOC and only on object
            tree = ET.parse(path_file)
            root = tree.getroot()
            xmin = root.find('object').find('bndbox').find('xmin')
            xmax = root.find('object').find('bndbox').find('xmax')
            xmin = int(xmin.text)
            xmax = int(xmax.text)
            x_ball = (xmax + xmin)/2

            ymin = root.find('object').find('bndbox').find('ymin')
            ymax = root.find('object').find('bndbox').find('ymax')
            ymin = int(ymin.text)
            ymax = int(ymax.text)
            y_ball = (ymax + ymin)/2
        else:
            x_ball = np.nan
            y_ball = np.nan
        
        data_points.append([x_ball, y_ball])

    data_points = np.array(data_points)
    data_points_interp = np.copy(data_points)


    # I guess its fine to consider x and y independent

    x_nans, x_points= nan_helper(data_points_interp[:,0])
    y_nans, y_points= nan_helper(data_points_interp[:,1])
    data_points_interp[x_nans,0]= np.interp(x_points(x_nans), x_points(~x_nans), data_points_interp[~x_nans, 0])
    data_points_interp[y_nans,1]= np.interp(y_points(y_nans), y_points(~y_nans), data_points_interp[~x_nans, 1])

    plt.plot(data_points, marker='o')
    plt.plot(data_points_interp, marker='+')
    plt.show()


    path_xy = path_folder / 'xy.csv'

    with open(path_xy, mode='w') as xy_file:
        xy_writer = csv.writer(xy_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        xy_writer.writerows(data_points)


create_xy_file()