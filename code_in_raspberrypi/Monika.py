from SignalGenerator import *
from Oscilloscope import *
from OscilloscopeApFFT import *
from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QStackedWidget,
                             QHBoxLayout, QListWidget)
from PyQt5.QtGui import QFont
import sys


class Monika(QWidget):
    def __init__(self):
        super().__init__()
        self.o = Oscilloscope()
        self.oa = OscilloscopeApFFT()
        self.s = SignalGenerator()
        self.topQStackedWidget = QStackedWidget(self)
        self.leftQListWidget = QListWidget()
        self.initUI()

    def initUI(self):
        def display(i):
            self.topQStackedWidget.setCurrentIndex(i)

        self.leftQListWidget.insertItem(0, '1.调制波形设置')
        self.leftQListWidget.insertItem(1, '2.FFT+CZT算法测频')
        self.leftQListWidget.insertItem(2, '3.全相位FFT算法测频')
        self.leftQListWidget.setFont(QFont('Serif', 20))
        self.leftQListWidget.currentRowChanged[int].connect(display)
        self.leftQListWidget.setMinimumSize(300, 1)
        self.leftQListWidget.setMaximumSize(300, 2000)

        self.topQStackedWidget.addWidget(self.s)
        self.topQStackedWidget.addWidget(self.o)
        self.topQStackedWidget.addWidget(self.oa)

        HBox = QHBoxLayout()
        HBox.addWidget(self.leftQListWidget)
        HBox.addWidget(self.topQStackedWidget)
        self.setLayout(HBox)
        cc = QDesktopWidget().availableGeometry()
        cc.setY(cc.top()+50)
        self.setGeometry(cc)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Monika()
    demo.show()
    sys.exit(app.exec_())
