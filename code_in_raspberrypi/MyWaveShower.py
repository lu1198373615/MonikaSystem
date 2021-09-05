from PyQt5.QtWidgets import (QWidget, QApplication, QGridLayout)
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from MyDataRom import *
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False


class MyWaveShower(QWidget):

    def __init__(self):
        super().__init__()
        self.f = 125000
        self.d = 15
        self.w = 1
        self.fig = plt.figure(figsize=(10, 4), dpi=80)
        self.canvas = FC(self.fig)
        self.ax = self.fig.add_subplot('111')
        self.ax.set_xlabel('UNIT : MicroSecond', fontsize=20)
        self.initUI()

    def set_value(self, f, d, w):
        self.f = f
        self.d = d
        self.w = w

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.canvas)
        self.setLayout(grid)
        self.resize(1000, 200)

    def paintEvent(self, e):
        self.ax.cla()
        x = np.arange(0, 1/self.f*32, 1/self.f/32)
        x = x * 1e6
        if self.w == 0:
            data = cos_rom
        if self.w == 1:
            data = tri_rom
        if self.w == 2:
            data = scan_up
        if self.w == 3:
            data = scan_dn
        data = np.concatenate((np.array(data), np.array(np.zeros(int(32/(self.d+1)*(15-self.d))))))
        y = np.array([])
        while 1:
            y = np.concatenate((y, data))
            if len(y) > 1024:
                break
        y = y[0:1024]
        self.ax.plot(x, y)
        self.ax.set_xlabel('UNIT : MicroSecond', fontsize=20, verticalalignment='bottom')
        self.canvas.draw()  # 绘制


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWaveShower()
    ex.show()
    sys.exit(app.exec_())
