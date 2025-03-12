import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QWidget

class Lines(QWidget):
    def __init__(self, ax, var_min, var_max, spacing, color='red'):
        super().__init__()
        self.ax = ax
        self.var_min = var_min
        self.var_max = var_max
        self.spacing = spacing
        self.color = color
        self.lines = []

        
        self.lines_vert = np.arange(self.var_min, self.var_max + self.spacing, self.spacing)
        self.lines_hor = np.arange(self.var_min, self.var_max + self.spacing, self.spacing)

    def create_horizontal_lines(self):
        x_values = np.arange(self.var_min, self.var_max + self.spacing, self.spacing)
        for x in x_values:
            line, = self.ax.plot([x, x], [self.var_min, self.var_max], color=self.color, linestyle='-') 
            self.lines.append(line)

    def create_vertical_lines(self):
        y_values = np.arange(self.var_min, self.var_max + self.spacing, self.spacing)
        for y in y_values:
            line, = self.ax.plot([self.var_min, self.var_max], [y, y], color=self.color, linestyle='-')
            self.lines.append(line)
        
    def get_pointshor(self):
        x = []
        y = []
        t = np.linspace(self.var_min, self.var_max, 101) 
        for x_pos in self.lines_vert:
            for i in t:
                x.append(x_pos)
                y.append(i) 

        return np.array(x), np.array(y)

    def get_pointsvert(self):
        x = []
        y = []  
        t = np.linspace(self.var_min, self.var_max, 101)
        for y_pos in self.lines_hor:
            for i in t:
                x.append(i)  
                y.append(y_pos)

        return np.array(x), np.array(y)
        
    