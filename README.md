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

## Instructions
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
| physics_steps_per_frame | 10                              | Changes the "frame rate", lower value means higher frame rate (not tested for values < 1)                                                                                                                                                                                                          |
| amount_cam_follow       | 0                               | Integer, amount of cameras that should follow the ball, starting from the first.                                                                                                                                                                                                                   |
| render_resolution_x     | 1280                            | Height of the rendered frame                                                                                                                                                                                                                                                                       |
| render_resolution_y     | 720                             | Width of the rendered frame                                                                                                                                                                                                                                                                        |
| set_fov                 | 24                              | Changes the field of view for all cameras.                                                                                                                                                                                                                                                         |
