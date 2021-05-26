import numpy as np
import DatasetGenerator
import DataManager

'''Add N cameras to both the camera_position and the camera_rotations file. Pay attention to use the same format as
given in the example files. The camera_rotations are given in xyz euler angles'''

camera_positions = np.loadtxt('camera_positions.csv', delimiter=",", skiprows=1)
camera_rotations = np.loadtxt('camera_rotations.csv', delimiter=",", skiprows=1)
assert camera_positions.shape[0] == camera_rotations.shape[0], 'Not the same amount of entries in \'camera_positions.csv\' as in \'camera_rotations.csv\''
dg = DatasetGenerator.DatasetGenerator()
dg.generate_dataset('test_run',
                    camera_positions,
                    camera_rotations,
                    steps=100,
                    save_frames=True,
                    write_video=True,
                    use_red_dot=False,
                    physics_steps_per_frame=10,
                    amount_cam_follow=1,
                    set_fov=24,
                    render_resolution_x=1920,
                    render_resolution_y=1080)
