from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QVBoxLayout, QWidget, QPushButton, QMessageBox, QLabel, QLineEdit, QHBoxLayout
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import math
from PyQt5.QtCore import Qt
import circumference as c
import rectangle as r
import graphic as g
import lines as l


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph = g.Graphic()
        self.setWindowTitle("Projeto Final")
        self.setGeometry(100, 100, 600, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        menubar = QMenuBar(self)
        self.setMenuBar(menubar)
        menubar.setStyleSheet("font-size: 18px;")

        menu = menubar.addMenu("Figura")
        self.selected_figure_option = None
        
        menu_fx = menubar.addMenu("f(x)")
        self.selected_fx_option = None
        
        self.button = QPushButton("Começar", self)
        self.button.clicked.connect(self.check_options)
        menubar.setCornerWidget(self.button, corner=Qt.TopRightCorner)

        opcoes_figura = ["Retas", "Quadrado", "Circunferência", "Desenhar"]
        for opcao in opcoes_figura:
            action = QAction(opcao, self)
            action.triggered.connect(lambda checked, opcao=opcao: self.selecionar_figura(opcao))
            menu.addAction(action)

        fx_opcoes = ["sen(x)", "cos(x)", "exp(x)", "z + 1/z"]
        for fx_opcao in fx_opcoes:
            action = QAction(fx_opcao, self)
            action.triggered.connect(lambda checked, fx_opcao=fx_opcao: self.selecionar_fx(fx_opcao))
            menu_fx.addAction(action)

        self.label = QLabel("Figura:  F(x):", self)
        self.layout.addWidget(self.label)
        self.show()
        
        self.figure1 = None
        self.figure2 = None

    def selecionar_figura(self, opcao):
        self.selected_figure_option = opcao
        self.update_label()

    def selecionar_fx(self, fx_opcao):
        self.selected_fx_option = fx_opcao
        self.update_label()

    def update_label(self):
        figura_text = f"Figura: {self.selected_figure_option}" if self.selected_figure_option else "Figura:"
        fx_text = f"F(x): {self.selected_fx_option}" if self.selected_fx_option else "F(x):"
        self.label.setText(f"{figura_text}  {fx_text}")

    def check_options(self):
        if self.selected_figure_option and self.selected_fx_option:
            try:
                self.update_window()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar a janela: {str(e)}")
        else:
            QMessageBox.critical(self, "Erro", "Selecione uma opção de cada menu.")

    def parse_input(self, input_str):
       
        try:
    
            input_str = input_str.replace("pi", str(math.pi))
        
            return np.array([float(eval(val)) for val in input_str.split(',')])
        except Exception as e:
            raise ValueError(f"Erro ao processar a entrada: {e}")

    def update_window(self):
        #fechar figuras antigas se existirem
        if self.figure1 is not None and self.figure2 is not None:
            plt.close(self.figure1)
            plt.close(self.figure2)
        
        #remover widgets anteriores, exceto o label principal
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None and widget != self.label:
                widget.setParent(None)

        #Remover o layout de inputs caso exista
        if hasattr(self, 'input_layout') and self.input_layout is not None:
            while self.input_layout.count():
                item = self.input_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            self.layout.removeItem(self.input_layout)
            self.input_layout = None

        self.figure1, self.ax1 = plt.subplots()
        canvas1 = FigureCanvas(self.figure1)
        self.layout.addWidget(canvas1)

        if self.selected_figure_option == "Retas":
            self.linesvert = l.Lines(self.ax1, -5,5, 0.5, 'red')
            self.lineshor = l.Lines(self.ax1, -5,5, 0.5, 'blue')
            self.linesvert.create_vertical_lines()
            self.lineshor.create_horizontal_lines()
            
            
           
        

        elif self.selected_figure_option == "Quadrado":
            self.rectangle = r.Rect(self.ax1, 0.1, 0.1, 0.5, 0.3, 'red')
     
            canvas1.mpl_connect("button_press_event", self.rectangle.on_button_press)
            canvas1.mpl_connect("button_release_event", self.rectangle.on_button_release)
            canvas1.mpl_connect("motion_notify_event", self.rectangle.on_mouse_move)

        elif self.selected_figure_option == "Circunferência":
            self.circumference = c.Circumference(self.ax1, -0.1, 0.5, 1, 'red')
            self.input_layout = QHBoxLayout()
            self.input_layout.addWidget(QLabel("Centro:"))
            center_input, radius_input = self.circumference.get_input()
            self.input_layout.addWidget(center_input)

            self.input_layout.addWidget(QLabel("Raio:"))
            self.input_layout.addWidget(radius_input)

            self.layout.addLayout(self.input_layout)
            self.show()
            canvas1.mpl_connect("button_press_event", self.circumference.on_button_press)
            canvas1.mpl_connect("button_release_event", self.circumference.on_button_release)
            canvas1.mpl_connect("motion_notify_event", self.circumference.on_mouse_move)

        elif self.selected_figure_option == "Desenhar":
            self.ax1.text(0.5, 0.5, "Modo de Desenho", fontsize=14, ha='center')

        canvas1.draw()
        
        
        self.figure2, self.ax2 = plt.subplots()
        canvas2 = FigureCanvas(self.figure2)
        self.layout.addWidget(canvas2)
        

        x = np.linspace(-5, 5, 100)
        

        if self.selected_fx_option == "sen(x)":
            if self.selected_figure_option == "Circunferência":
                x,y = self.circumference.get_points()
                xs,ys = self.graph.calcular_sen(x, y)
                self.ax2.plot(xs, ys, label="sen(z)", color='purple')
            elif self.selected_figure_option == "Quadrado":
                x ,y = self.rectangle.get_points()
                xs,ys = self.graph.calcular_sen(x, y)
                self.ax2.plot(xs, ys, label="sen(z)", color='purple')
            elif self.selected_figure_option == "Retas":   
                x,y = self.linesvert.get_pointsvert()
                xs,ys = self.graph.calcular_sen(x,y)
                self.ax2.plot(xs, ys, label="sen(z)", color='red')
                z,m = self.lineshor.get_pointshor()
                zs,ms = self.graph.calcular_sen(z,m)
                self.ax2.plot(zs, ms, label="sen(z)", color='blue')
            else:
                self.ax2.plot(x, np.sin(x), label="sen(x)", color='blue')
                

        elif self.selected_fx_option == "cos(x)":
            if self.selected_figure_option == "Circunferência":
                x,y = self.circumference.get_points()
                xs,ys = self.graph.calcular_cos(x,y)
                self.ax2.plot(xs, ys, label="cos(z)", color='green')
            elif self.selected_figure_option == "Quadrado":
                x ,y = self.rectangle.get_points()
                xs,ys = self.graph.calcular_cos(x,y)
                self.ax2.plot(xs, ys, label="cos(z)", color='green')
            elif self.selected_figure_option == "Retas":
                x,y = self.linesvert.get_pointsvert()
                xs,ys = self.graph.calcular_cos(x,y)
                self.ax2.plot(xs, ys, label="cos(z)", color='red')
                z,m = self.lineshor.get_pointshor()
                zs,ms = self.graph.calcular_cos(z,m)
                self.ax2.plot(zs, ms, label="cos(z)", color='blue')
            else:
                self.ax2.plot(x, np.cos(x), label="cos(x)", color='green')

        
        elif self.selected_fx_option == "exp(x)":
            if self.selected_figure_option == "Circunferência":
                x,y = self.circumference.get_points()
                xs,ys = self.graph.calcular_exp(x,y)
                self.ax2.plot(xs, ys, label="exp(z)", color='red')
            elif self.selected_figure_option == "Quadrado":
                x ,y = self.rectangle.get_points()
                xs,ys = self.graph.calcular_exp(x,y)
                self.ax2.plot(xs, ys, label="exp(z)", color='red')
            elif self.selected_figure_option == "Retas":
                x,y = self.linesvert.get_pointsvert()
                xs,ys = self.graph.calcular_exp(x,y)     
                self.ax2.plot(xs, ys, label="exp(z)", color='red')
                plt.gca().set_aspect('equal', adjustable='box')
                z,m = self.lineshor.get_pointshor()
                zs,ms = self.graph.calcular_exp(z,m)    
                self.ax2.plot(zs, ms, label="exp(z)", color='blue')
            else:
                self.ax2.plot(x, np.exp(x), label="exp(x)", color='red')


        elif self.selected_fx_option == "z + 1/z":
            if self.selected_figure_option == "Circunferência":
                x,y = self.circumference.get_points()
                xs,ys = self.graph.calcular_z_mais_1_por_z(x, y)
                self.ax2.plot(xs, ys, label="z + 1/z", color='orange')
            elif self.selected_figure_option == "Quadrado":
                x ,y = self.rectangle.get_points()
                xs,ys = self.graph.calcular_z_mais_1_por_z(x, y)
                self.ax2.plot(xs, ys, label="z + 1/z", color='orange')
            elif self.selected_figure_option == "Retas":
                x,y = self.lines.get_pointsvert()
                xs,ys = self.graph.calcular_z_mais_1_por_z(x, y)
                self.ax2.plot(xs, ys, label="z + 1/z", color='red')
                z,m = self.lines.get_pointshor()
                zs,ms = self.graph.calcular_z_mais_1_por_z(z,m)
                self.ax2.plot(zs, ms, label="z + 1/z", color='blue')
            else:
                self.ax2.plot(x, x + 1/x, label="z + 1/z", color='orange')

        self.ax2.legend()
        canvas2.draw()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
