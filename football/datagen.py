import numpy as np
import DatasetGenerator
import DataManager

camera_positions = np.loadtxt('camera_positions.csv', delimiter=",", skiprows=1)
camera_rotations = np.loadtxt('camera_rotations.csv', delimiter=",", skiprows=1)

dg = DatasetGenerator.DatasetGenerator()
dg.generate_dataset('test_run.csv',
                    camera_positions,
                    camera_rotations,
                    steps=200,
                    save_frames=True,
                    write_video=True,
                    use_red_dot=False,
                    physics_steps_per_frame=10,
                    amount_cam_follow=1,
                    set_fov=24)
