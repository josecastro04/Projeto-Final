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
        self.lines_hor = []
        self.lines_vert = []
        self.update_lineshori(spacing)
        self.update_linesvert(spacing)  
        

    def create_horizontal_lines(self):
        
        for y in self.lines_hor:
            line, = self.ax.plot([self.x_min, self.x_max], [y, y], color='blue', linestyle='-')
            self.lines.append(line)

    def create_vertical_lines(self):
        for x in self.lines_vert:
            line, = self.ax.plot([x, x], [self.y_min, self.y_max], color='red', linestyle='-')
            self.lines.append(line)
            
    def clear_lines(self):
    
        for line in self.lines:
            if line in self.ax.lines:
                line.remove()
        self.lines.clear()
        self.lines_hor = np.array([])
        self.lines_vert = np.array([])

    def update_lineshori(self,new_spacing):
        self.spacing = new_spacing
        num_hor = int((self.y_max - self.y_min) / self.spacing) + 1
        self.lines_hor = np.linspace(self.y_min, self.y_max , num_hor)
        self.num_pontos = self.calcula_num_pontos()
        for line in self.ax.lines[:]:
            line.remove()
        
        self.create_horizontal_lines()
        
        self.ax.figure.canvas.draw()
        
    def update_linesvert(self,new_spacing):
        self.spacing = new_spacing
        num_vert = int((self.x_max - self.x_min) / self.spacing) + 1
        self.lines_vert = np.linspace(self.x_min, self.x_max , num_vert)
        self.num_pontos = self.calcula_num_pontos()
        for line in self.ax.lines[:]:
            line.remove()
     
        
        self.create_vertical_lines()
        self.ax.figure.canvas.draw()
   

    def calcula_num_pontos(self):
       
        x = self.x_max - self.x_min
        y = self.y_max - self.y_min
        return int(max(x, y) * 50)

    def get_pointshor(self):
        
        x = []
        y = []
        t = np.linspace(self.x_min, self.x_max, self.num_pontos)  
        for y_pos in self.lines_hor:
            for i in t:
                x.append(i)  
                y.append(y_pos)  
        return np.array(x), np.array(y)

    def get_pointsvert(self):
       
        x = []
        y = []  
        t = np.linspace(self.y_min, self.y_max, self.num_pontos)  
        for x_pos in self.lines_vert:
            for i in t:
                x.append(x_pos)  
                y.append(i)  
        return np.array(x), np.array(y)

    def plot_on_ax2(self, ax2, xs, ys, zs, ms):
        
        segmentos_verticais = [
            np.column_stack([xs[i:i+self.num_pontos], ys[i:i+self.num_pontos]]) 
            for i in range(0, len(xs), self.num_pontos)
        ]

        segmentos_horizontais = [
            np.column_stack([zs[i:i+self.num_pontos], ms[i:i+self.num_pontos]]) 
            for i in range(0, len(zs), self.num_pontos)
        ]

        lc_verticais = LineCollection(segmentos_verticais, colors='red')
        lc_horizontais = LineCollection(segmentos_horizontais, colors='blue')

        return lc_verticais, lc_horizontais
