import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projeto Final")
        self.setGeometry(100, 100, 1600, 600)
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
         
        layout = QHBoxLayout(central_widget)
             
        self.figure1, self.ax1 = plt.subplots()
        canvas1 = FigureCanvas(self.figure1)    
        
        layout.addWidget(canvas1)
           
        y_values = [1, 2, 3, 4, 5] 
        for y in y_values:
            self.ax1.axhline(y=y, color='blue', linestyle='-')
        
        x_values = [1, 2, 3, 4, 5] 
        for x in x_values:
            self.ax1.axvline(x=x, color='red', linestyle='-')
        
        canvas1.draw()
        
        y_cosseno = np.cos(y_values)  
        x_cosseno = np.cos(x_values)

        self.figure2, self.ax2 = plt.subplots()
        canvas2 = FigureCanvas(self.figure2)
        
        layout.addWidget(canvas2)
        
        self.ax2.plot(y_values, y_cosseno, label='cos(y) para as linhas azuis', color='blue', marker='o')
        self.ax2.plot(x_values, x_cosseno, label='cos(x) para as linhas vermelhas', color='red', marker='x')
          
        self.ax2.legend()
            
        canvas2.draw()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
