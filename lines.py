import numpy as np
from matplotlib.collections import LineCollection
from PyQt5.QtWidgets import QWidget

class Lines(QWidget):
    def __init__(self, ax, x_min, x_max, y_min, y_max, spacing, color):
        super().__init__()
        self.ax = ax
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.spacing = spacing
        self.color = color
        self.lines = []

        self.lines_vert = np.arange(self.x_min, self.x_max + self.spacing, self.spacing)
        self.lines_hor = np.arange(self.y_min, self.y_max + self.spacing, self.spacing)

    def create_horizontal_lines(self):
        for y in self.lines_hor:
            line, = self.ax.plot([self.x_min, self.x_max], [y, y], color=self.color, linestyle='-')
            self.lines.append(line)

    def create_vertical_lines(self):
        for x in self.lines_vert:
            line, = self.ax.plot([x, x], [self.y_min, self.y_max], color=self.color, linestyle='-')
            self.lines.append(line)

    def get_pointshor(self):
        x = []
        y = []
        t = np.linspace(self.x_min, self.x_max, 101)  
        for y_pos in self.lines_hor:
            for i in t:
                x.append(i)  
                y.append(y_pos)  
        return np.array(x), np.array(y)

    def get_pointsvert(self):
        x = []
        y = []  
        t = np.linspace(self.y_min, self.y_max, 101)  
        for x_pos in self.lines_vert:
            for i in t:
                x.append(x_pos)  
                y.append(i)  
        return np.array(x), np.array(y)
    def plot_on_ax2(self, ax2, xs, ys, zs, ms):
       
        num_pontos = 101
        segmentos_verticais = [
            np.column_stack([xs[i:i+num_pontos], ys[i:i+num_pontos]]) 
            for i in range(0, len(xs), num_pontos)
        ]

        segmentos_horizontais = [
            np.column_stack([zs[i:i+num_pontos], ms[i:i+num_pontos]]) 
            for i in range(0, len(zs), num_pontos)
        ]

        lc_verticais = LineCollection(segmentos_verticais, colors='red')
        lc_horizontais = LineCollection(segmentos_horizontais, colors='blue')

        return lc_verticais, lc_horizontais