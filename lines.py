import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QWidget

class Lines(QWidget):
    def __init__(self, ax, x_min=-5, x_max=5, spacing=1.5, color='red', color2='blue'):
        super().__init__()
        self.ax = ax
        self.x_min = x_min
        self.x_max = x_max
        self.spacing = spacing
        self.color = color
        self.color2 = color2
        self.lines = []

        self.create_vertical_lines()
        self.create_horizontal_lines()
        
        self.lines_vert = np.arange(self.x_min, self.x_max + self.spacing, self.spacing)
        self.lines_hor = np.arange(self.x_min, self.x_max + self.spacing, self.spacing)

    def create_vertical_lines(self):
        x_values = np.arange(self.x_min, self.x_max + self.spacing, self.spacing)
        for x in x_values:
            line, = self.ax.plot([x, x], [-5, 5], color=self.color, linestyle='-') 
            self.lines.append(line)

    def create_horizontal_lines(self):
        y_values = np.arange(self.x_min, self.x_max + self.spacing, self.spacing)
        for y in y_values:
            line, = self.ax.plot([-5, 5], [y, y], color=self.color2, linestyle='-')
            self.lines.append(line)
        
    def get_pointsvert(self):
        x = []
        y = []
        perimeter = 10  
        t = np.linspace(0, perimeter, 100) 
        for x_pos in self.lines_vert:
            for i in t:
                x.append(x_pos)
                y.append(-5 + i) 

        return np.array(x), np.array(y)

    def get_pointshor(self):
        x = []
        y = []
        perimeter = 10  
        t = np.linspace(0, perimeter, 100)
        for y_pos in self.lines_hor:
            for i in t:
                x.append(-5 + i)  
                y.append(y_pos)

        return np.array(x), np.array(y)
        
    