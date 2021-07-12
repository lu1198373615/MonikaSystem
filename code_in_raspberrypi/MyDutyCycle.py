from PyQt5.QtWidgets import (QWidget, QSlider, QApplication, QDesktopWidget, QLabel, QGridLayout,
                             QHBoxLayout, QVBoxLayout, QSpinBox)
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
import sys


class MyDutyCycle(QWidget):
    updateBW = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.initUI()

    def get_duty_cycle(self):
        return self.fff

    def initUI(self):

        def update_label():
            dutyCycleQLabel.setText('占空比\n=' + str(dutyCycleQSlider.value() * 6.25) + '%')
            self.fff = dutyCycleQSlider.value() - 1
            self.updateBW.emit(self.fff)

        dutyCycleQSlider = QSlider(Qt.Horizontal)
        dutyCycleQSlider.setFocusPolicy(Qt.NoFocus)
        dutyCycleQSlider.setMinimumSize(1, 100)
        dutyCycleQSlider.setStyleSheet("QWidget { background-color: #ffffb8 }")
        dutyCycleQSlider.setRange(1, 16)
        dutyCycleQSlider.setValue(16)
        dutyCycleQSlider.valueChanged.connect(update_label)

        dutyCycleQLabel = QLabel()
        dutyCycleQLabel.setFont(QFont('Serif', 20))
        dutyCycleQLabel.setAlignment(Qt.AlignCenter)
        dutyCycleQLabel.setMinimumSize(200, 1)
        dutyCycleQLabel.setMaximumSize(200, 500)
        dutyCycleQLabel.setStyleSheet("QWidget { background-color: #ffffb8 }")

        update_label()

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(dutyCycleQSlider, 1, 1, 1, 2)
        grid.addWidget(dutyCycleQLabel, 1, 3, 1, 1)

        self.setLayout(grid)
        self.resize(1000, 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyDutyCycle()
    ex.show()
    print(ex.get_duty_cycle())
    sys.exit(app.exec_())


