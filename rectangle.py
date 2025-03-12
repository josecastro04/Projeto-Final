import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

class Rect:
    def __init__(self, ax, x, y, width, height, color):
        self.ax = ax
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.rectangle = Rectangle((self.x, self.y), self.width, self.height, color=self.color, fill=False)
        self.ax.add_patch(self.rectangle)
        
        self.center_x = self.x + self.width / 2
        self.center_y = self.y + self.height / 2

        self.center_point, = self.ax.plot(self.center_x, self.center_y, 'or')

        self.point_x = self.x
        self.point_y = self.y + self.height

        self.control_point, = self.ax.plot(self.point_x, self.point_y, 'ob')

        self.toggle_center_point = False
        self.toggle_control_point = False

    def get_point(self, event):
        return np.hypot(self.point_x - event.xdata, self.point_y - event.ydata) <= 0.05

    def get_center(self, event):
        return np.hypot(self.center_x - event.xdata, self.center_y - event.ydata) <= 0.05

    def on_button_press(self, event):
        if event.xdata is None or event.ydata is None:
            return
        elif self.get_point(event):
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
            distance_x = self.point_x - event.xdata
            distance_y = self.point_y - event.ydata

            self.point_x = event.xdata
            self.point_y = event.ydata

            self.height -= distance_y
            self.width += distance_x

            self.x = self.point_x

            self.rectangle.set_x(self.x)
            self.rectangle.set_height(self.height)
            self.rectangle.set_width(self.width)
        elif self.toggle_center_point:
            distance_x = self.center_x - event.xdata
            distance_y = self.center_y - event.ydata

            self.x -= distance_x
            self.y -= distance_y

            self.point_x = self.x
            self.point_y = self.y + self.height
            self.rectangle.set_xy((self.x, self.y))

        self.center_x, self.center_y = self.rectangle.get_center()
        self.center_point.set_xdata([self.center_x])
        self.center_point.set_ydata([self.center_y])

        self.control_point.set_xdata([self.point_x])
        self.control_point.set_ydata([self.point_y])


        plt.draw()

    def get_points(self):
        perimeter = 2 * (self.width + self.height)
        t = np.linspace(0, perimeter, 200)
        x = []
        y = []

        for i in t:
            if i < self.width:
                x.append(self.x + i)
                y.append(self.y)
            elif i < self.width + self.height:
                x.append(self.x + self.width)
                y.append(self.y + (i - self.width))
            elif i < 2 * self.width + self.height:
                x.append(self.x + self.width - (i - self.width - self.height))
                y.append(self.y + self.height)
            else:
                x.append(self.x)
                y.append(self.y + self.height - (i - 2 * self.width - self.height))

        return np.array(x), np.array(y)
