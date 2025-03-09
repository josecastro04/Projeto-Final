import numpy as np  
class Graphic:
    def __init__(self):
        pass  
    def calcular_sen(self, x, y):
        xs = []
        ys = []
        for i in range(len(x)):
            xs.append(np.sin(x[i]) * np.cosh(y[i]))
            ys.append(np.cos(x[i]) * np.sinh(y[i]))
        return xs, ys

    def calcular_cos(self, x,y):
        xs = []
        ys = []
        for i in range(len(x)):
            xs.append(np.cos(x[i]) * np.cosh(y[i]))
            ys.append(-np.sin(x[i]) * np.sinh(y[i]))
        return xs, ys

    def calcular_exp(self, x,y):
        xs = []
        ys = []
        for i in range(len(x)):
            xs.append(np.exp(x[i]) * np.cos(y[i]))
            ys.append(np.exp(x[i]) * np.sin(y[i]))
        return xs, ys

    def calcular_z_mais_1_por_z(self, x, y):
        xs = []
        ys = []
        for i in range(len(x)):
            xs.append(x[i] * (x[i] ** 2 + y[i] ** 2 + 1) / (x[i] ** 2 + y[i] ** 2))
            ys.append(y[i] * (x[i] ** 2 + y[i] ** 2 - 1) / (x[i] ** 2 + y[i] ** 2))
        return xs, ys
