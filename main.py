from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QSlider,QMainWindow, QMenu, QMenuBar, QAction, QVBoxLayout, QWidget, QPushButton, QMessageBox, QLabel, QLineEdit, QHBoxLayout
from matplotlib.widgets import RangeSlider, Slider
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QComboBox

import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import circumference as c
import rectangle as r
import graphic as g
import lines as l
from matplotlib.collections import LineCollection


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

        opcoes_figura = ["Grelhas", "Retângulo", "Circunferência", "Desenhar"]
        for opcao in opcoes_figura:
            action = QAction(opcao, self)
            action.triggered.connect(lambda checked, opcao=opcao: self.selecionar_figura(opcao))
            menu.addAction(action)

        fx_opcoes = ["sen(x)", "cos(x)", "exp(x)", "z + 1/z"]
        for fx_opcao in fx_opcoes:
            action = QAction(fx_opcao, self)
            action.triggered.connect(lambda checked, fx_opcao=fx_opcao: self.selecionar_fx(fx_opcao))
            menu_fx.addAction(action)

        self.label = QLabel(self)
        self.label.setText("<b>Figura:</b>  <b>F(x):</b>  ")

        self.layout.addWidget(self.label, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.label.setStyleSheet("font-size: 16px; padding: 4px;")

        self.show()
        
        self.figure1 = None
        self.figure2 = None
        self.figure3 = None

    def selecionar_figura(self, opcao):
        self.selected_figure_option = opcao
        self.update_label()

    def selecionar_fx(self, fx_opcao):
        self.selected_fx_option = fx_opcao
        self.update_label()

    def update_label(self):
        figura_text = f"<b>Figura:</b> {self.selected_figure_option}" if self.selected_figure_option else "<b>Figura:</b>"
        fx_text = f"<b>F(x):</b> {self.selected_fx_option}" if self.selected_fx_option else "<b>F(x):</b>"
        self.label.setText(f"{figura_text}  {fx_text}")

    def check_options(self):
        if self.selected_figure_option and self.selected_fx_option:
            try:
                self.update_window()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar a janela: {str(e)}")
        else:
            QMessageBox.critical(self, "Erro", "Selecione uma opção de cada menu.")
    
    def update_window(self):
        
        if self.figure1 is not None and self.figure2 is not None:
            plt.close(self.figure1)
            plt.close(self.figure2)
        
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None and widget != self.label:
                widget.setParent(None)

        
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
        
        if self.selected_figure_option == "Grelhas":
            self.figure3 = Figure()  
            self.canvas3 = FigureCanvas(self.figure3)
            self.canvas3.setVisible(False)
            self.layout.addWidget(self.canvas3)
            
            self.x_min, self.x_max, self.y_min, self.y_max, self.spacing = -1, 2, 0, 3, 0.25
            

            self.linesvert = l.Lines(self.ax1, self.x_min, self.x_max, self.y_min, self.y_max, self.spacing, 'red')
            self.lineshor = l.Lines(self.ax1, self.x_min, self.x_max, self.y_min, self.y_max, self.spacing, 'blue')
            self.linesvert.create_vertical_lines()
            self.lineshor.create_horizontal_lines()

            self.ax1.set_xlim(self.x_min, self.x_max)
            self.ax1.set_ylim(self.y_min, self.y_max)
            
            
            self.add_sliders()
            self.show()
        elif self.selected_figure_option == "Retângulo":
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
        self.ax1.set_aspect('equal')
        
        self.figure2, self.ax2 = plt.subplots()
        canvas2 = FigureCanvas(self.figure2)
        self.layout.addWidget(canvas2)  

        x = np.linspace(-5, 5, 100)

        if self.selected_fx_option == "sen(x)":
            if self.selected_figure_option == "Circunferência":
                x, y = self.circumference.get_points()
                xs, ys = self.graph.calcular_sen(x, y)
                self.ax2.plot(xs, ys, label="sen(z)", color='purple')
            elif self.selected_figure_option == "Retângulo":
                x, y = self.rectangle.get_points()
                xs, ys = self.graph.calcular_sen(x, y)
                self.ax2.plot(xs, ys, label="sen(z)", color='purple')
            elif self.selected_figure_option == "Grelhas":
                x, y = self.linesvert.get_pointsvert()
                xs, ys = self.graph.calcular_sen(x, y)
                z, m = self.lineshor.get_pointshor()
                zs, ms = self.graph.calcular_sen(z, m)

                lc_verticais, lc_horizontais = self.linesvert.plot_on_ax2(self.ax2, xs, ys, zs, ms)

                self.ax2.add_collection(lc_verticais)
                self.ax2.add_collection(lc_horizontais)
                self.ax2.plot([], [], ' ', label="sen(z)")  
            else:
                self.ax2.plot(x, np.sin(x), label="sen(x)", color='blue')
        elif self.selected_fx_option == "cos(x)":
            if self.selected_figure_option == "Circunferência":
                x,y = self.circumference.get_points()
                xs,ys = self.graph.calcular_cos(x,y)
                self.ax2.plot(xs, ys, label="cos(z)", color='green')
            elif self.selected_figure_option == "Retângulo":
                x ,y = self.rectangle.get_points()
                xs,ys = self.graph.calcular_cos(x,y)
                self.ax2.plot(xs, ys, label="cos(z)", color='green')
            elif self.selected_figure_option == "Grelhas":
                x, y = self.linesvert.get_pointsvert()
                xs, ys = self.graph.calcular_cos(x, y)
                z, m = self.lineshor.get_pointshor()
                zs, ms = self.graph.calcular_cos(z, m)

                lc_verticais, lc_horizontais = self.linesvert.plot_on_ax2(self.ax2, xs, ys, zs, ms)

                self.ax2.add_collection(lc_verticais)
                self.ax2.add_collection(lc_horizontais)
                self.ax2.plot([], [], ' ', label="cos(z)")
            else:
                self.ax2.plot(x, np.cos(x), label="cos(x)", color='green')   
        elif self.selected_fx_option == "exp(x)":
            if self.selected_figure_option == "Circunferência":
                x,y = self.circumference.get_points()
                xs,ys = self.graph.calcular_exp(x,y)
                self.ax2.plot(xs, ys, label="exp(z)", color='red')
            elif self.selected_figure_option == "Retângulo":
                x ,y = self.rectangle.get_points()
                xs,ys = self.graph.calcular_exp(x,y)
                self.ax2.plot(xs, ys, label="exp(z)", color='red')
            elif self.selected_figure_option == "Grelhas":
                x,y = self.linesvert.get_pointsvert()
                xs,ys = self.graph.calcular_exp(x,y)     
                z,m = self.lineshor.get_pointshor()
                zs,ms = self.graph.calcular_exp(z,m)    
                

                lc_verticais, lc_horizontais = self.linesvert.plot_on_ax2(self.ax2, xs, ys, zs, ms)

                self.ax2.add_collection(lc_verticais)
                self.ax2.add_collection(lc_horizontais)
                self.ax2.plot([], [], ' ', label="exp(z)")     
            else:
                self.ax2.plot(x, np.exp(x), label="exp(x)", color='red')
        elif self.selected_fx_option == "z + 1/z":
            if self.selected_figure_option == "Circunferência":
                x,y = self.circumference.get_points()
                xs,ys = self.graph.calcular_z_mais_1_por_z(x, y)
                self.ax2.plot(xs, ys, label="z + 1/z", color='orange')
            elif self.selected_figure_option == "Retângulo":
                x ,y = self.rectangle.get_points()
                xs,ys = self.graph.calcular_z_mais_1_por_z(x, y)
                self.ax2.plot(xs, ys, label="z + 1/z", color='orange')
            elif self.selected_figure_option == "Grelhas":
                x,y = self.linesvert.get_pointsvert()
                xs,ys = self.graph.calcular_z_mais_1_por_z(x, y)
                
                z,m = self.lineshor.get_pointshor()
                zs,ms = self.graph.calcular_z_mais_1_por_z(z,m)
                

                lc_verticais, lc_horizontais = self.linesvert.plot_on_ax2(self.ax2, xs, ys, zs, ms)

                self.ax2.add_collection(lc_verticais)
                self.ax2.add_collection(lc_horizontais)
                self.ax2.plot([], [], ' ', label="z + 1/z")
            else:
                self.ax2.plot(x, x + 1/x, label="z + 1/z", color='orange')

        self.ax2.set_aspect('equal')
        self.ax2.legend()
        canvas2.draw()
    
    def add_sliders(self):
        self.figure3.clear()
        
        combo_espacamento = QComboBox()
        combo_espacamento.addItems(["Selecione...", "Espaçamento Horizontal", "Espaçamento Vertical"])
        combo_espacamento.currentTextChanged.connect(self.selecionar_espacamento)

        layout_espacamento = QVBoxLayout()
        layout_espacamento.addWidget(QLabel("Alterar Espaçamento:"))
        layout_espacamento.addWidget(combo_espacamento)

        combo_tamanho = QComboBox()
        combo_tamanho.addItems(["Selecione...", "Alterar tamanho Reta Horizontal", "Alterar tamanho Reta Vertical"])
        combo_tamanho.currentTextChanged.connect(self.selecionar_opcao)

        layout_tamanho = QVBoxLayout()
        layout_tamanho.addWidget(QLabel("Alterar Tamanho:"))
        layout_tamanho.addWidget(combo_tamanho)

       
        menu_layout = QVBoxLayout()
        menu_layout.addLayout(layout_espacamento)
        menu_layout.addLayout(layout_tamanho)

        menu_widget = QWidget()
        menu_widget.setLayout(menu_layout)

        hbox = QHBoxLayout()
        hbox.addWidget(menu_widget)
        
        hbox.setContentsMargins(30, 5, 30, 5)
        hbox.setSpacing(15)

        slider_widget = QWidget()
        slider_widget.setLayout(hbox)
        self.layout.addWidget(slider_widget)

    def show_error_message(self):
        QMessageBox.warning(self, "Erro", "Selecione uma reta para alterar antes de usar o slider.")

    def selecionar_opcao(self, opcao):
        self.update_label()

        if opcao == "Selecione...":
           return
       
        self.canvas3.setVisible(True)

        if hasattr(self, 'slider_ax2') and self.slider_ax2 in self.figure3.axes:
            self.figure3.delaxes(self.slider_ax2)
       
        self.slider_ax2 = self.figure3.add_axes([0.1, 0.2, 0.8, 0.15]) 
        
        if opcao == "Alterar tamanho Reta Horizontal":
            valinit = (self.lineshor.x_min, self.lineshor.x_max)
            range_min, range_max = self.lineshor.x_min, self.lineshor.x_max
        elif opcao == "Alterar tamanho Reta Vertical":
            valinit = (self.linesvert.y_min, self.linesvert.y_max)
            range_min, range_max = self.linesvert.y_min, self.linesvert.y_max
        else:
            return

        self.slider_length = RangeSlider(self.slider_ax2, "Tamanho das Linhas", -10, 10, valinit=(range_min,range_max), valstep=1)
        self.slider_length.on_changed(lambda val: self.update_lines(val, opcao))

        self.canvas3.draw()

    def selecionar_espacamento(self, opcao):
        if opcao == "Selecione...":
           return
       
        self.canvas3.setVisible(True)
    
        if hasattr(self, 'slider_ax3') and self.slider_ax3 in self.figure3.axes:
           self.figure3.delaxes(self.slider_ax3)
    
        self.slider_ax3 = self.figure3.add_axes([0.1, 0.05, 0.8, 0.15])  
    
        if opcao == "Espaçamento Horizontal":
           valinit_aux = self.lineshor.spacing
           self.numero_linhas = (self.lineshor.x_max - self.lineshor.x_min) / self.spacing
           
           label = "Espaçamento Horizontal"
        elif opcao == "Espaçamento Vertical":
           valinit_aux = self.linesvert.spacing
           self.numero_linhas = (self.linesvert.y_max - self.linesvert.y_min) / self.spacing
           label = "Espaçamento Vertical"
        else:
            return
        
        self.slider_spacing = Slider(self.slider_ax3, label, 1, 20, valinit=self.numero_linhas, valstep=1)
        self.slider_spacing.on_changed(lambda val: self.update_spacing(val, opcao))
    
        self.canvas3.draw()


       
    def update_spacing(self, val, tipo):
        """Atualiza o espaçamento horizontal ou vertical diretamente"""
        if tipo == "Espaçamento Horizontal":
            self.numero_linhas = val
            self.lineshor.spacing = (self.lineshor.x_max - self.lineshor.x_min) / self.numero_linhas
            self.lineshor.clear_lines()  
            self.lineshor.update_lineshori(self.lineshor.spacing)
            self.linesvert.create_vertical_lines() 
            self.ax1.set_xlim(self.lineshor.x_min, self.lineshor.x_max)
        elif tipo == "Espaçamento Vertical":
            self.numero_linhas = val
            self.linesvert.spacing = (self.linesvert.y_max - self.linesvert.y_min) / self.numero_linhas
            self.linesvert.clear_lines() 
            self.linesvert.update_linesvert(self.linesvert.spacing)
            self.lineshor.create_horizontal_lines()
            self.ax1.set_ylim(self.linesvert.y_min, self.linesvert.y_max)
        self.figure1.canvas.draw()

        self.ax2.clear()
        self.ax2.grid(True)

      
        if self.selected_fx_option == "sen(x)":
            function = self.graph.calcular_sen
        elif self.selected_fx_option == "cos(x)":
            function = self.graph.calcular_cos
        elif self.selected_fx_option == "exp(x)":
            function = self.graph.calcular_exp
        else:
            function = self.graph.calcular_z_mais_1_por_z

        x, y = self.linesvert.get_pointsvert()
        xs, ys = function(x, y)
        z, m = self.lineshor.get_pointshor()
        zs, ms = function(z, m)

        lc_verticais, lc_horizontais = self.linesvert.plot_on_ax2(self.ax2, xs, ys, zs, ms)
        self.ax2.add_collection(lc_verticais)
        self.ax2.add_collection(lc_horizontais)
        self.ax2.plot([], [], ' ', label="Transformação f(z)")
        self.ax2.legend()
        self.figure2.canvas.draw()

    def update_lines(self, val,opcao):
        """Atualiza o tamanho das linhas e atualiza os gráficos"""
        if self.selected_figure_option == "Grelhas":
            if opcao == "Alterar tamanho Reta Horizontal":
                self.lineshor.x_min, self.lineshor.x_max = self.slider_length.val
                self.linesvert.x_min, self.linesvert.x_max = self.slider_length.val
                for line in self.ax1.lines[:]:
                    line.remove()

                self.lineshor.create_horizontal_lines()
                self.linesvert.create_vertical_lines()

                self.ax1.set_xlim(self.lineshor.x_min, self.lineshor.x_max)
                self.ax1.set_ylim(self.lineshor.y_min, self.lineshor.y_max)  
            elif opcao == "Alterar tamanho Reta Vertical":
                self.linesvert.y_min, self.linesvert.y_max = self.slider_length.val
                self.lineshor.y_min, self.lineshor.y_max = self.slider_length.val 
                for line in self.ax1.lines[:]:
                    line.remove()
                    
                self.linesvert.create_vertical_lines()
                self.lineshor.create_horizontal_lines()
                self.ax1.set_ylim(self.linesvert.y_min, self.linesvert.y_max)

                self.ax1.set_xlim(self.linesvert.x_min, self.linesvert.x_max)
              
            self.figure1.canvas.draw()
              
            self.ax2.clear()
            self.ax2.grid(True)

            if self.selected_fx_option == "sen(x)":
                  function = self.graph.calcular_sen
            elif self.selected_fx_option == "cos(x)":
                  function = self.graph.calcular_cos
            elif self.selected_fx_option == "exp(x)":
                  function = self.graph.calcular_exp
            else:
                  function = self.graph.calcular_z_mais_1_por_z

            x, y = self.linesvert.get_pointsvert()
            xs, ys = function(x, y)
            z, m = self.lineshor.get_pointshor()
            zs, ms = function(z, m)

            lc_verticais, lc_horizontais = self.linesvert.plot_on_ax2(self.ax2, xs, ys, zs, ms)
            self.ax2.add_collection(lc_verticais)
            self.ax2.add_collection(lc_horizontais)
            self.ax2.plot([], [], ' ', label="Transformação f(z)")
            self.ax2.legend()
            self.figure2.canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()