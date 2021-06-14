# -*- coding: utf-8 -*-
"""
Visualize the trajectory or points
"""

import vispy
from vispy.scene import visuals, SceneCanvas

import numpy as np
import time
import cv2

class SoccerVisualizer():
    def __init__(self, camera_position=[0, 0, 0]):
        """ visualizer for a football game

        Args:
            camera_position (list 1x3, optional): [camera position at start]. Defaults to [-20, 50, 20].
        
        LMB: orbits the view around its center point.

        RMB or scroll: change scale_factor (i.e. zoom level)

        SHIFT + LMB: translate the center point

        SHIFT + RMB: change FOV
        """

        self.canvas = SceneCanvas(title='Soccer Field', keys='interactive', show=True)
        self.grid = self.canvas.central_widget.add_grid()
        self.view = vispy.scene.widgets.ViewBox(border_color='black', parent=self.canvas.scene)
        self.grid.add_widget(self.view, 0, 0)

        
        self.view.camera = vispy.scene.cameras.TurntableCamera( up='z', azimuth=170)
        self.view.camera.center = camera_position

        self.tick = 0
        self.old_time = None
    

        
        visuals.XYZAxis(parent=self.view.scene)

        '''
        Draw Soccer Field for reference [IMAGE VERSION]
        '''
        field = cv2.imread('field.png')[13:394,27:613,0]
        field[field>0] = 255
        field_size = np.shape(field)
        football_field = visuals.Image(data = field[:,:].T, parent = self.view.scene, cmap='grays')
        center_trans = vispy.visuals.transforms.MatrixTransform()
        center_trans.translate((-field_size[0]/2, -field_size[1]/2, 0))
        center_trans.scale(scale=(105/field_size[1], 68/field_size[0], 1))
        center_trans.rotate(90,(0,0,1))
        football_field.transform = center_trans



    def draw_ball_marker(self, positions, color, size_marker, timer=False, sampling_rate=800/16.17):
        """
        Ball Visualizer (for now with a marker)

        Parameters
        ----------
        positions : 3xN array containing ball positions,Origin at center of field, x is width, y is length
        color: color of the ball, eg. red for triangulated, blue for ground truth¨
        real_time: (False) if true tries to do it in real time with given sampling rate
        sampling_rate (float, optional): [sampling rate of your input positions]. Defaults to 800/16.17.
        
        Returns
        -------
        None.
        """
        if timer is False:
            ball_vis = visuals.Markers()
            ball_vis.set_data(positions, size=size_marker, face_color=color, edge_color=color)
            self.view.add(ball_vis)
        else:
            # auto is 1/60 seconds
            self.ball_positions = positions
            self.color_ball = color
            self.size_marker = size_marker
            self.timer = app.Timer( connect=self.on_timer, start=False)
            

        self.view.update()

    def on_timer(self, event):
        """ timer for animation

        Args:
            event (vispy event): look at the vispy documentation
        """
        if self.old_time is None:
            self.old_time = time.time()
            self.span = 1
        else:
            delta = time.time() - self.old_time
            self.old_time = time.time()
            print(delta)
            self.span = self.sampling_rate*delta

        t = int(self.tick)
        t_span = int(self.span+self.tick)
        self.draw_ball_marker(np.array(self.ball_positions[t:t_span]), self.color_ball, self.size_marker)
        
        self.tick += self.span
        self.canvas.update()

        if self.tick > self.ball_positions.shape[0]:
            self._timer.disconnect()


    #def draw_ball_sphere(self, position, color, size_sphere):

    def draw_3d_line(self, points, color):
        Plot3D = vispy.scene.visuals.create_visual_node(vispy.visuals.LinePlotVisual)

        pos = np.c_[points[0], points[1], points[2]]
        Plot3D(pos, width=1000.0, color=color, edge_color='w', parent=self.view.scene)




if __name__ == '__main__':
    
    visualizer = SoccerVisualizer()
    '''
    Test Ball
    '''
    ball_pos = np.array([[2, 4, 3]])

    
    visualizer.draw_ball_marker(ball_pos, color='red', size_marker=10)
    vispy.app.run()