from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QLabel, QGridLayout, QComboBox,
                             QSpinBox, QPushButton)
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QFont
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from MyDataRom import *
import matplotlib.pyplot as plt
from MyWSPI import *
from MyWiringPiSPI import *
from CZTAlgorithm import *
plt.rcParams['axes.unicode_minus'] = False


class Oscilloscope(QWidget):
    def __init__(self):
        super().__init__()
        self.s = MyWiringPiSPI()
        self.w = MyWSPI()
        self.c = CZTAlgorithm()
        self.resultQLabel = QLabel('频率为:')
        self.f_sample = 100e6
        self.point_sample = 1
        self.timer = QBasicTimer()
        #self.timer.start(2000, self)
        if self.timer.isActive():
            self.timer.stop()
        self.fig = plt.figure(figsize=(10, 4), dpi=80)
        self.canvas = FC(self.fig)
        self.ax = self.fig.add_subplot('111')
        self.ax.set_xlabel('UNIT : MicroSecond', fontsize=20)
        self.ax.axis(ymin=-2100, ymax=2100)
        self.initUI()

    def initUI(self):
        def update_param(sss):
            self.point_sample = int(sss)
            print(self.point_sample)
        def update_gain(g):
            self.s.trans_reg([5,int((g+5)/3)])

        rateQLabel = QLabel('采样频率选择')
        rateQLabel.setFont(QFont('Serif', 20))
        rateQLabel.setAlignment(Qt.AlignCenter)
        rateQLabel.setMinimumSize(200, 1)
        rateQLabel.setMaximumSize(200, 500)
        rateQLabel.setStyleSheet("QWidget { background-color: #ffffb8 }")

        rateQComoBox = QComboBox(self)
        rateQComoBox.addItem("100MSPS")
        rateQComoBox.setFont(QFont('Serif', 30))
        rateQComoBox.setMinimumSize(200, 1)
        rateQComoBox.setMaximumSize(200, 500)
        rateQComoBox.setStyleSheet("QWidget { background-color: #ffffb8 }")
        
        gainQLabel = QLabel('AD8369\n增益选择(dB)')
        gainQLabel.setFont(QFont('Serif', 20))
        gainQLabel.setAlignment(Qt.AlignCenter)
        gainQLabel.setMinimumSize(200, 1)
        gainQLabel.setMaximumSize(200, 500)
        gainQLabel.setStyleSheet("QWidget { background-color: #ffffb8 }")
        
        gainQSpinBox = QSpinBox()
        gainQSpinBox.setRange(-5, 40)  # 设置范围
        gainQSpinBox.setSingleStep(3)  # 设置步长
        gainQSpinBox.setValue(-5)  # 设置spinbox的值
        update_gain(-5)
        gainQSpinBox.setFont(QFont('Serif', 30))
        gainQSpinBox.setMinimumSize(200, 1)
        gainQSpinBox.setMaximumSize(200, 500)
        gainQSpinBox.setStyleSheet("QWidget { background-color: #ffffb8 }")
        gainQSpinBox.valueChanged[int].connect(update_gain)

        pointQLabel = QLabel('相参积累次数')
        pointQLabel.setFont(QFont('Serif', 20))
        pointQLabel.setAlignment(Qt.AlignCenter)
        pointQLabel.setMinimumSize(200, 1)
        pointQLabel.setMaximumSize(200, 500)
        pointQLabel.setStyleSheet("QWidget { background-color: #ffffb8 }")

        pointQComoBox = QComboBox(self)
        pointQComoBox.addItem("1")
        pointQComoBox.addItem("10")
        pointQComoBox.addItem("50")
        pointQComoBox.addItem("100")
        pointQComoBox.setFont(QFont('Serif', 30))
        pointQComoBox.setMinimumSize(200, 1)
        pointQComoBox.setMaximumSize(200, 500)
        pointQComoBox.setStyleSheet("QWidget { background-color: #ffffb8 }")
        pointQComoBox.activated[str].connect(update_param)
        
        self.resultQLabel.setFont(QFont('Serif', 40))
        self.resultQLabel.setAlignment(Qt.AlignCenter)
        self.resultQLabel.setMinimumSize(800, 1)
        self.resultQLabel.setMaximumSize(800, 500)
        self.resultQLabel.setStyleSheet("QWidget { background-color: #ffffb8 }")
        
        self.switchQPushButton = QPushButton('Start', self)
        self.switchQPushButton.setFont(QFont('Serif', 30))
        self.switchQPushButton.setMinimumSize(200, 1)
        self.switchQPushButton.setMaximumSize(200, 500)
        self.switchQPushButton.setStyleSheet("QWidget { background-color: #ff0000 }")
        self.switchQPushButton.clicked.connect(self.doAction)
        
        grid = QGridLayout()
        grid.addWidget(self.resultQLabel, 1, 1, 1, 1)
        grid.addWidget(self.switchQPushButton, 1, 2, 1, 1)
        grid.addWidget(self.canvas, 2, 1, 5, 2)
        grid.addWidget(rateQLabel, 1, 3, 1, 1)
        grid.addWidget(rateQComoBox, 2, 3, 1, 1)
        grid.addWidget(gainQLabel, 3, 3, 1, 1)
        grid.addWidget(gainQSpinBox, 4, 3, 1, 1)
        grid.addWidget(pointQLabel, 5, 3, 1, 1)
        grid.addWidget(pointQComoBox, 6, 3, 1, 1)
        cc = QDesktopWidget().availableGeometry()
        cc.setY(cc.top()+50)
        self.setGeometry(cc)
        self.setLayout(grid)
        self.setWindowTitle('Oscilloscope')
        self.my_paint()

    def my_paint(self):
        self.ax.cla()
        y = self.w.fifo_sample(int(self.point_sample*400))
        x = np.linspace(0, (len(y)-1)/self.f_sample, len(y))
        x = x * 1e6
        self.ax.plot(np.real(x), np.real(y))
        self.ax.set_xlabel('UNIT : MicroSecond', fontsize=20, verticalalignment='bottom')
        self.ax.axis(ymin=-2100, ymax=2100)
        self.canvas.draw()  # 绘制
        hp = self.c.fft_czt(y)
        di = hp*6/1e6
        self.resultQLabel.setText('频率为: ' + '%.1f Hz' % hp)

    def timerEvent(self, e):
        self.my_paint()
    
    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.switchQPushButton.setText('Start')
            self.switchQPushButton.setStyleSheet("QWidget { background-color: #ff0000 }")
        else:
            self.timer.start(1000, self)
            self.switchQPushButton.setText('Stop')
            self.switchQPushButton.setStyleSheet("QWidget { background-color: #00ff00 }")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Oscilloscope()
    ex.show()
    sys.exit(app.exec_())
