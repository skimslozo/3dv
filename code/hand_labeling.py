import cv2

from pathlib import Path


video_path = Path.cwd().parent / 'football_data' / 'EPTS - Camera 1.mp4'
vidcap = cv2.VideoCapture(str(video_path))
success,image = vidcap.read()


count = 0
path_folder = Path.cwd().parent / 'football_data' / 'hand_labeled'
path_folder.mkdir(parents=True, exist_ok=False)

while success:
    path = path_folder / ('frame' + str(count) + '.jpg')
    print(path)
    cv2.imwrite(str(path), image)     # save frame as JPEG file      
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    count += 1