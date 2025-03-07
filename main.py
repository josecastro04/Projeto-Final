from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QVBoxLayout, QWidget, QPushButton, QMessageBox, QLabel, QLineEdit, QHBoxLayout
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import math
from PyQt5.QtCore import Qt
import circumference as c
import rectangle as r

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

        fx_opcoes = ["sen(x)", "cos(x)", "exp(x)", "1/2 (1 + 1/x)"]
        for fx_opcao in fx_opcoes:
            action = QAction(fx_opcao, self)
            action.triggered.connect(lambda checked, fx_opcao=fx_opcao: self.selecionar_fx(fx_opcao))
            menu_fx.addAction(action)

        self.label = QLabel("Figura:  F(x):", self)
        self.layout.addWidget(self.label)
        self.show()

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
            # Avalia a string como expressão matemática
            return np.array([float(eval(val)) for val in input_str.split(',')])
        except Exception as e:
            raise ValueError(f"Erro ao processar a entrada: {e}")

    def update_window(self):
        
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None and widget != self.label:
                widget.deleteLater()

        self.figure1, self.ax1 = plt.subplots()
        canvas1 = FigureCanvas(self.figure1)
        self.layout.addWidget(canvas1)

        if self.selected_figure_option == "Retas":
            for y in y_values:
                self.ax1.axhline(y=y, color='blue', linestyle='-')

            for x in x_values:
                self.ax1.axvline(x=x, color='red', linestyle='-')

        elif self.selected_figure_option == "Quadrado":
            self.rectangle = r.Rect(self.ax1, 0.1, 0.1, 0.5, 0.3, 'red')
     
            canvas1.mpl_connect("button_press_event", self.rectangle.on_button_press)
            canvas1.mpl_connect("button_release_event", self.rectangle.on_button_release)
            canvas1.mpl_connect("motion_notify_event", self.rectangle.on_mouse_move)

        elif self.selected_figure_option == "Circunferência":
            self.circumference = c.Circumference(self.ax1, 0.5, 0.5, 0.2, 'red')
            input_layout = QHBoxLayout()
            input_layout.addWidget(QLabel("Centro:"))
            center_input, radius_input = self.circumference.get_input()
            input_layout.addWidget(center_input)

            input_layout.addWidget(QLabel("Raio:"))
            input_layout.addWidget(radius_input)

            self.layout.addLayout(input_layout)
            self.show();
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
            self.ax2.plot(x, np.sin(x), label="sen(x)", color='blue')
        elif self.selected_fx_option == "cos(x)":
            self.ax2.plot(x, np.cos(x), label="cos(x)", color='red')
        elif self.selected_fx_option == "exp(x)":
            self.ax2.plot(x, np.exp(x), label="exp(x)", color='green')
        elif self.selected_fx_option == "1/2 (1 + 1/x)":
            x_valid = x[x != 0]  
            self.ax2.plot(x_valid, 0.5 * (1 + 1 / x_valid), label="1/2 (1 + 1/x)", color='purple')

        self.ax2.legend()
        canvas2.draw()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
