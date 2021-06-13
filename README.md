<p align="left" width="100%">
  <img height="100" src="img/topbar.png"> &nbsp; &nbsp; 
</p>

# 3D Vision Project: Soccer Ball Detection and Tracking
## Marian, Jason, Miks & Jannik

### Important Links

* [Google Docs with work packages](https://docs.google.com/document/d/1t3td3Fl85A2u-0nMh3fmjDndkqI4slvDTglgTJUZuDA/edit)
* [Proposal Presentation](https://docs.google.com/presentation/d/1S16nQzCUljWjCPs96GXUtMhLLvK8xuvwSQWkcADmUa8/edit#slide=id.p)
* [Project Proposal Outline](https://docs.google.com/document/d/17Tfdv_uZz8P1Bmt9VpqbMHXWcxzVBZuWPozLdoFZHRE/edit
)
* [Project Propsal: Latex](https://www.overleaf.com/project/60489a2f4a789faf8b9b6a97)
* [Paper Presentation Slides](https://docs.google.com/presentation/d/1S3GxRsPdXZiqShj0OZToLz6usqU2533UunqTbY_e2UY/edit#slide=id.p)
* [Tracking without Bells and Whistles Paper](https://arxiv.org/pdf/1903.05625.pdf)
* [Meeting Notes](https://docs.google.com/presentation/d/1Qc-awR3Rm8LvFofIlVhyMQX5Vdfm6IE92jTrVlCi2Co/edit#slide=id.gccea4da259_0_415)
* [Midterm Presentation Slides](https://docs.google.com/presentation/d/1muzkyLSw_7Nf9fOaegXsPI-R6865XZPMH31HjMHUhFw/edit#slide=id.gd2ad2b4450_5_3)
* [Hand Label Pictures](https://github.com/qaprosoft/labelImg)
* [Final Paper Outline](https://docs.google.com/document/d/186wmasgGrZnZuw9eYNlKpqqP2u3gKj774uPydnajW0o/edit?usp=sharing)
* [Final Paper Overleaf](https://www.overleaf.com/project/60a10867b143f70445357d6f)
* [Final Presentation](https://docs.google.com/presentation/d/1BE0HA_Y6XRBG14XwHTo9m5vSwsqMllhRKUUvcAC5g6w/edit#slide=id.gdd7fd61593_0_0)

To set up google football simulation go to https://github.com/google-research/football

## Project Managment 
In general, for every task do a github issue

## Quick Start 

tested on ubuntu 20.04

#### 1. Install required packages
```
pip3 install -r requirements.txt
```
to install the visualizer and data generator



#### 2. Install required packages for football simulator
```
sudo apt-get install git cmake build-essential libgl1-mesa-dev libsdl2-dev \
libsdl2-image-dev libsdl2-ttf-dev libsdl2-gfx-dev libboost-all-dev \
libdirectfb-dev libst-dev mesa-utils xvfb x11vnc libsdl-sge-dev python3-pip
```

#### 3. Installing from source

```
cd football
```


The last step is to build the environment:

```
pip3 install .
```
This command can run for a couple of minutes, as it compiles the C++ environment in the background.

#### 3. Generate Data

```
cd src/
python3 datagen.py
```



## Instructions
### Dataset Generation
To generate a dataset navigate into the '/football' directory where there is a file called 'datagen.py'. 
The script in 'datagen.py', when run, will automatically generate a dataset in a folder contained in this repository's 
root folder called 'football_data'. 

Also, to be found in the '/football' directory are two .csv files, 'camera_positions.csv' and 'camera_rotation.csv'. In
these one can define the cameras for which data should be generated, this is done by automatically running the same 
deterministic football game in the simulator with these defined camera positions and rotations. 
The lines in these two files represent the same cameras position and rotation respectively. The rotations are to be
given in xyz Euler angles. Please assert that for each camera defined in 'camera_positions.csv' you also have a rotation
defined in 'camera_rotations.csv'. The origin for positions is in the center of the field. 

The 'datagen.py' script calls a function that generates all data automatically. Here you can set various parameters
for the dataset.

| Parameter               | Default                         | Explanation                                                                                                                                                                                                                                                                                        |
|-------------------------|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| run_name                | -                               | Name of the run, a directory with the data will be generated.                                                                                                                                                                                                                                      |
| cam_positions           | -                               | Nx3 array containing the positions of N different cameras. (read from the csv)                                                                                                                                                                                                                     |
| cam_rotations           | -                               | Nx3 array containing the rotation (xyz Euler angles) of N different cameras. (read from the csv)                                                                                                                                                                                                   |
| level                   | 'tests.11_vs_11 _deterministic' | What deterministic scenario should be used. Options can be found in football/gfootball/scenarios/test . IMPORTANT: if you want to use a scenario that does not have the ending '_deterministic', open the  scenario file and insure that the flag 'builder.config().deterministic' is set to True! |
| steps                   | 100                             | Amount of steps (frames) the simulation should make.                                                                                                                                                                                                                                               |
| render                  | True                            | If true, the pygame window will appear and render the game (slower). (Necessary for 'save_frames')                                                                                                                                                                                                 |
| save_frames             | True                            | If true, the frames of the game will be saved.                                                                                                                                                                                                                                                     |
| write_video             | False                           | If true, a video will be made from the frames. ('save_frames' need to be True)                                                                                                                                                                                                                     |
| use_red_dot             | False                           | If true, a red dot will be rendered on each frame to highlight the ball.                                                                                                                                                                                                                           |
| physics_steps_per_frame | 1                               | Changes the "frame rate", lower value means higher frame rate (not tested for values < 1) (only 1 will give perfectly accurate 2D pixel positions)                                                                                                                                                 |
| amount_cam_follow       | 0                               | Integer, amount of cameras that should follow the ball, starting from the first.                                                                                                                                                                                                                   |
| render_resolution_x     | 1280                            | Height of the rendered frame                                                                                                                                                                                                                                                                       |
| render_resolution_y     | 720                             | Width of the rendered frame                                                                                                                                                                                                                                                                        |
| set_fov                 | 24                              | Changes the field of view for all cameras.                                                                                                                                                                                                                                                         |

### Working with the Dataset
The easiest way to work with this data is to use our DataManager class. With it one can load in the data with 
ease and is given many getter and data modification methods to work with. The getter methods returns the data in a way 
that makes it easy to work with it in an efficient vectorized manner. An example of this is the 
datamanager.get_proj_mat_all() function which will return an MxNx3x4 array, containing projection Matrices of the shape 
3x4 , where M is the number of cameras and N is the amount of steps. Here the DataManager internally already calculated 
the projection matrix for you. Further the DataManager is able to add noise to the pixel coordinates, the intrinsic 
matrix, the extrinsic matrix and the projection matrix. 


## File Struture
- football/ containts a hard fork from https://github.com/google-research/football with major changes
- src/ contains the dataset generator and the rest of the pipeline
  1. DataManager.py saves all data
  2. DatasetGenerator.py activates the football/ folder
  3. EstimationMetric.py consists several estimation metrics
  4. SoccerVisualizer.py to visualize football field and trajectory
  5. TrajectoryEstimation.py estimatior for trajectory
  6. Explore_Dataset.py Example of Triangulation on dataset 'test_run2'
  7. camera_positions.csv contains camera position for datagen.py
  8. camera_orientation.csv contains camera orientation for datagen.py
  9. datagen.py to generate data. Entry Point
  10. field.png field used by visualizer
  11. hand_labeling.py tool to interpolate hand labeled data and also to go from video to frames
  12. noise_analysis.py noise vs multiple cameras based on dataset 'run_mari2'
  13. test_DataManager.py tester for data manager
  14. triangulate_handlabeled.py visiualize the hand-labeled data
  15. triangulatepoints.py contains method to triangulate points based on camera parameters
- img/ general image fro illustration and report
- data/ data used for report
  1. 
