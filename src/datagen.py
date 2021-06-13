import numpy as np
import DatasetGenerator

'''
    Add N cameras to both the camera_position.csv and the camera_rotations.csv file. Pay attention to use the same 
    format as given in the example files. The camera_rotations are to be given in xyz euler angles.
'''

camera_positions = np.loadtxt('camera_positions.csv', delimiter=",", skiprows=1)
camera_rotations = np.loadtxt('camera_rotations.csv', delimiter=",", skiprows=1)
assert camera_positions.shape[0] == camera_rotations.shape[0], 'Not the same amount of entries in ' \
                                                               '\'camera_positions.csv\' as in \'camera_rotations.csv\''
dg = DatasetGenerator.DatasetGenerator()

"""
        Automatically generate a data set for one game with multiple camera views. Will be saved in a directory in the
        parent directory called 'football_data'.

        Parameters
        ----------
        run_name : Name of the run, a directory with the data will be generated.
        cam_positions : Nx3 array containing the positions of N different cameras.
        cam_rotations: Nx3 array containing the rotation (xyz Euler angles) of N different cameras.
        level: what deterministic scenario should be used. Options can be found in football/gfootball/scenarios/test .
        IMPORTANT: if you want to use a scenario that does not have the ending '_deterministic', open the scenario file
        and insure that the flag 'builder.config().deterministic' is set to True!
        steps : Amount of steps the simulation should make
        render : if true the pygame window will appear and render the game (slower)
        save_frames : if true the frames of the game will be saved
        write_video : if true a video will be made from the frames, should only be true when save_frames is true
        use_red_dot: if True puts a red point in the frame where the ball is according to the pixel coordinates
        physics_steps_per_frame: 1 (Default). only tested with physics_steps_per_frame=1, higher values work but the 
        2d pixel positions wont be perfect. 
        amount_cam_follow: amount of cameras that should follow the ball, starting from the first.
        render_resolution_x: Height of the rendered frame20Brains-Gan356#
        render_resolution_y: Width of the rendered frame
        set_fov: Changes the field of view of all cameras
"""
dg.generate_dataset('test_run',
                    camera_positions,
                    camera_rotations,
                    level='tests.11_vs_11_deterministic',  # read instructions above before changing!
                    steps=300,
                    save_frames=True,
                    write_video=True,
                    use_red_dot=False,
                    physics_steps_per_frame=1,
                    amount_cam_follow=1,
                    set_fov=24,
                    render_resolution_x=1920,
                    render_resolution_y=1080)
