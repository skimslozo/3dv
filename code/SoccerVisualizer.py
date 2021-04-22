# -*- coding: utf-8 -*-
"""
Visualize the trajectory or points
"""

import vispy
from vispy.scene import visuals, SceneCanvas

import numpy as np
import cv2

class SoccerVisualizer():
    def __init__(self):
        self.canvas = SceneCanvas(title='Soccer Field', keys='interactive', show=True)
        self.grid = self.canvas.central_widget.add_grid()
        self.view = vispy.scene.widgets.ViewBox(border_color='black', parent=self.canvas.scene)
        self.grid.add_widget(self.view, 0, 0)
        
        self.view.camera = vispy.scene.cameras.TurntableCamera(up='z', azimuth=90)
        '''
        LMB: orbits the view around its center point.

        RMB or scroll: change scale_factor (i.e. zoom level)

        SHIFT + LMB: translate the center point

        SHIFT + RMB: change FOV
        '''
        
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

    def draw_ball_marker(self, positions, color, size_marker):
        """
        Ball Visualizer (for now with a marker)

        Parameters
        ----------
        positions : 3xN array containing ball positions,Origin at center of field, x is width, y is length
        color: color of the ball, eg. red for triangulated, blue for ground truth
        Returns
        -------
        None.
        """
        ball_vis = visuals.Markers()
        ball_vis.set_data(positions, size=size_marker, face_color=color, edge_color=color)
        self.view.add(ball_vis)

    #def draw_ball_sphere(self, position, color, size_sphere):


if __name__ == '__main__':
    
    visualizer = SoccerVisualizer()
    '''
    Test Ball
    '''
    ball_pos = np.array([[2, 4, 3]])
    
    visualizer.draw_ball_marker(ball_pos, color='red', size_marker=10)
    vispy.app.run()