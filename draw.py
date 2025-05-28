import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
from PyQt5.QtCore import Qt  # Importar Qt

class Draw:
    def __init__(self, ax, canvas):
        self.ax = ax
        self.canvas = canvas
        self.coord = []
        self.points = []
        self.lines = []
        self.labels = []
        self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
        
        self.ax.grid()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        
        self.canvas.mpl_connect('button_press_event', self.onclick)
        self.canvas.mpl_connect('key_press_event', self.on_key)
        
        ax_button = plt.axes([0.8, 0.05, 0.1, 0.075])
        self.btn_reset = Button(ax_button, 'Reset')
        self.btn_reset.on_clicked(self.reset)
        
        # Adicionar estas linhas para garantir que o canvas tenha foco
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()

    def onclick(self, event):
        if event.xdata is not None and event.ydata is not None:
            x, y = event.xdata, event.ydata
            self.coord.append((x, y))

            point, = self.ax.plot(x, y, 'bo', markersize=5)
            self.points.append(point)
            label = self.ax.annotate(f'({x:.2f}, {y:.2f})', (x, y), textcoords="offset points", xytext=(5,5), ha='right')
            self.labels.append(label)

            self.canvas.draw_idle()

    def on_key(self, event):
        if event.key == 'enter' and len(self.coord) > 1:
            x_vals, y_vals = zip(*self.coord)

            line = Line2D(x_vals + (x_vals[0],), y_vals + (y_vals[0],), color='black')
            self.ax.add_line(line)
            self.lines.append(line)

            self.canvas.draw_idle()

    def reset(self, event):
        self.coord.clear()

        for point in self.points:
            point.remove()
        self.points.clear()

        for line in self.lines:
            line.remove()
        self.lines.clear()

        for label in self.labels:
            label.remove()
        self.labels.clear()

        self.canvas.draw_idle()
        
    def get_points(self):
        return self.coord
