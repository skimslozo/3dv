
# create game
# game is not determistic 


from gfootball.env import config
from gfootball.env import football_action_set
from gfootball.env import football_env
from gfootball.env import observation_processor

from PIL import Image, ImageDraw

import copy
import six.moves.cPickle
import os
import tempfile
import numpy as np
from scipy.spatial.transform import Rotation as R


def load_dump(dump_file):
    dump = []
    with open(dump_file, 'rb') as in_fd:
        while True:
            try:
                step = six.moves.cPickle.load(in_fd)
            except EOFError:
                return dump
            dump.append(step)

def __modify_trace(replay, fps):
    """Adopt replay to the new framerate and add additional steps at the end."""
    trace = []
    min_fps = replay[0]['debug']['config']['physics_steps_per_frame']
    assert fps % min_fps == 0, (
        'Trace has to be rendered in framerate being multiple of {}'.format(
            min_fps))
    assert fps <= 100, ('Framerate of up to 100 is supported')
    empty_steps = int(fps / min_fps) - 1
    for f in replay:
      trace.append(f)
      idle_step = copy.deepcopy(f)
      idle_step['debug']['action'] = [football_action_set.action_idle
                                     ] * len(f['debug']['action'])
      for _ in range(empty_steps):
        trace.append(idle_step)
    # Add some empty steps at the end, so that we can record videos.
    for _ in range(10):
      trace.append(idle_step)
    return trace

def __build_players(dump_file, spec):
    players = []
    for player in spec:
      players.extend(['replay:path={},left_players=1'.format(
          dump_file)] * config.count_left_players(player))
      players.extend(['replay:path={},right_players=1'.format(
          dump_file)] * config.count_right_players(player))
    return players

def _replay(dump, fps, output_path, x_rot, x_cam, y_cam, z_cam):

    # I dont recomand to change this
    FOV = 24
    config_update={}
    render = True
    directory= None

    replay = load_dump(dump)
    trace = __modify_trace(replay, fps)
    fd, temp_path = tempfile.mkstemp(suffix='.dump')
    with open(temp_path, 'wb') as f:
      for step in trace:
        six.moves.cPickle.dump(step, f)
    assert replay[0]['debug']['frame_cnt'] == 0, (
        'Trace does not start from the beginning of the episode, can not replay')
    cfg = config.Config(replay[0]['debug']['config'])
    cfg['players'] = __build_players(temp_path, cfg['players'])
    config_update['physics_steps_per_frame'] = int(100 / fps)
    config_update['real_time'] = False
    if directory:
      config_update['tracesdir'] = directory
    config_update['write_video'] = True
    cfg.update(config_update)
    env = football_env.FootballEnv(cfg)
    if render:
      env.render()
    env.reset()
    done = False

    camrot = np.array([x_rot, 0, 0]) # handy to set the camera coordinates in Euler angles
    r = R.from_euler('xyz', camrot, degrees = True)
    carot_quat = r.as_quat()
    step = 1

    s_cam = str(x_cam)+'-'+ str(y_cam)+'-'+ str(z_cam)+'-'+str(x_rot)+'.txt'

    with open(output_path + s_cam, 'a') as f:
        f.write('camera orientation in Euler Angles ' + str(camrot)+'\n')
        f.write('camera position in x, y, z    ' + str(x_cam)+','+ str(y_cam)+','+ str(z_cam)+',' +'\n')
        f.write('camera FOV ' + str(FOV)+'\n')
        f.write('step,x,y \n')
        try:
            while not done:
                env._env._env.set_camera_node_orientation(-0.0, -0.0, -0.0, 1.0)
                env._env._env.set_camera_node_position(x_cam, y_cam, z_cam)
                env._env._env.set_camera_orientation(carot_quat[0], carot_quat[1], carot_quat[2], carot_quat[3])
                env._env._env.set_camera_fov(FOV)
                
                obs, _, done, _ = env.step([])
                frame = obs['frame']
                x, y = env._env._env.get_pixel_coordinates()
                img = Image.fromarray(frame.astype('uint8'))

                img.save(output_path + str(step)+'.png', format='png')
                img.close()
                
                f.write(str(step)+','+str(x)+','+str(y)+'\n')
                step = step + 1
        except KeyboardInterrupt:
            env.write_dump('shutdown')
            exit(1)
    os.close(fd)

# import gfootball.env as football_env
# env = football_env.create_environment(env_name="11_vs_11_stochastic", stacked=False, logdir='tmp/football', write_goal_dumps=False, write_full_episode_dumps=True, render=False)
# env.reset()
# steps = 0
# while True:
#   obs, rew, done, info = env.step(env.action_space.sample())
#   steps += 1
#   if steps % 100 == 0:
#     print("Step %d Reward: %f" % (steps, rew))
#   if done:
#     break


# load file
dump = '/home/pdesolver/3dv/tmp/football/episode_done_20210505-010734603773.dump'

output_path = '/home/pdesolver/3dv/tmp/football/fast/cam10/'
fps = 10

_replay(dump, fps, output_path, 50, 0, -80, 60)

print('done!')

quit()


output_path = '/home/pdesolver/3dv/tmp/football/fast/cam2/'
fps = 10

_replay(dump, fps, output_path, 50, 40, -100, 80)
print('done!')

output_path = '/home/pdesolver/3dv/tmp/football/fast/cam3/'
fps = 10

_replay(dump, fps, output_path, 0, 0, 0, 80)
print('done!')


output_path = '/home/pdesolver/3dv/tmp/football/slow/cam1/'
fps = 100

_replay(dump, fps, output_path, 50, -40, -100, 80)
print('done!')

output_path = '/home/pdesolver/3dv/tmp/football/slow/cam2/'
fps = 100

_replay(dump, fps, output_path, 50, 40, -100, 80)
print('done!')

output_path = '/home/pdesolver/3dv/tmp/football/slow/cam3/'
fps = 100

_replay(dump, fps, output_path, 0, 0, 0, 80)
print('done!')