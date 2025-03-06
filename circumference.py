import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class Circumference:
    def __init__(self, ax, x, y, radius, color):
        self.ax = ax
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.circle = Circle((self.x, self.y), self.radius, color=self.color, fill=False)
        self.ax.add_patch(self.circle)

        self.point_x = x + np.cos(np.pi / 4) * self.radius
        self.point_y = y + np.sin(np.pi / 4) * self.radius

        self.control_point, = self.ax.plot(self.point_x, self.point_y, 'ob')
        self.center_point, = self.ax.plot(self.x, self.y, 'og')

        self.toggle_center_point = False
        self.toggle_control_point = False

        self.ax.set(xlim=(-4,4), ylim=(-4,4))

    def get_point(self, event):
        return np.hypot(self.point_x - event.xdata, self.point_y - event.ydata) <= 0.05

    def get_center(self, event):
        return np.hypot(self.x - event.xdata, self.y - event.ydata) <= 0.05

    def on_button_press(self, event):
        if event.xdata is None or event.ydata is None:
            return 
        if self.get_point(event):
            self.toggle_control_point = True
        elif self.get_center(event):
            self.toggle_center_point = True
    
    def on_button_release(self, event):
        self.toggle_control_point = False
        self.toggle_center_point = False

    def on_mouse_move(self, event):
        if event.xdata is None or event.ydata is None:
            return 

        if self.toggle_control_point:
            self.radius = np.hypot(self.x - event.xdata, self.y - event.ydata)
            self.circle.set_radius(self.radius)
        elif self.toggle_center_point:
            self.x = event.xdata
            self.y = event.ydata
            self.circle.set_center((self.x, self.y))
            self.center_point.set_xdata([self.x])
            self.center_point.set_ydata([self.y])

        self.point_x = self.x + np.cos(np.pi / 4) * self.radius
        self.point_y = self.y + np.sin(np.pi / 4) * self.radius
        self.control_point.set_xdata([self.point_x])
        self.control_point.set_ydata([self.point_y])
        
        plt.draw()
    

