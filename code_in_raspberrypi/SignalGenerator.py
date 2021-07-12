from MyFrequency import *
from MyDutyCycle import *
from MyWaveSelector import *
from MyWaveShower import *
from MyWiringPiSPI import *

from PyQt5.QtWidgets import (QWidget, QSlider, QApplication, QDesktopWidget, QLabel, QGridLayout,
                             QHBoxLayout, QVBoxLayout, QSpinBox)
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
import sys


class SignalGenerator(QWidget):

    def __init__(self):
        super().__init__()
        self.f = MyFrequency()
        self.d = MyDutyCycle()
        self.w = MyWaveSelector()
        self.s = MyWaveShower()
        self.m = MyWiringPiSPI()
        self.param_changed()
        self.initUI()

    def initUI(self):
        self.f.updateBW.connect(self.param_changed)
        self.d.updateBW.connect(self.param_changed)
        self.w.updateBW.connect(self.param_changed)
        exQVBoxLayout = QVBoxLayout()
        exQVBoxLayout.addWidget(self.f)
        exQVBoxLayout.addWidget(self.d)
        exQVBoxLayout.addWidget(self.w)
        exQVBoxLayout.addWidget(self.s)
        self.setLayout(exQVBoxLayout)
        self.setWindowTitle('DDS Signal Generator')
        cc = QDesktopWidget().availableGeometry()
        cc.setY(cc.top()+50)
        self.setGeometry(cc)
        self.param_changed()
        self.show()

    def param_changed(self):
        f = self.f.get_frequency()
        d = self.d.get_duty_cycle()
        w = self.w.get_wave_type()
        self.s.set_value(f, d, w)
        self.s.repaint()
        self.m.set_wave(f,d,w)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SignalGenerator()
    sys.exit(app.exec_())
