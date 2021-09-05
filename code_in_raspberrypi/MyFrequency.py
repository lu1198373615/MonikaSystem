from PyQt5.QtWidgets import (QWidget, QSlider, QApplication, QLabel, QGridLayout,)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import sys


class MyFrequency(QWidget):
    updateBW = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.initUI()

    def get_frequency(self):
        return self.fff

    def initUI(self):

        def update_label():
            integerQLabel.setText(str(integerQSlider.value()) + '    X')
            d = {1: '1Hz', 2: '10Hz', 3: '100Hz', 4: '1kHz', 5: '10kHz'}
            unitQLabel.setText(d.get(unitQSlider.value()))
            frequencyQLabel.setText('频率\n=' + str(integerQSlider.value() * 10 ** (unitQSlider.value()-1)) + 'Hz')
            self.fff = integerQSlider.value() * 10 ** (unitQSlider.value()-1)
            self.updateBW.emit(self.fff)

        integerQSlider = QSlider(Qt.Horizontal)
        integerQSlider.setFocusPolicy(Qt.NoFocus)
        integerQSlider.setMinimumSize(800, 100)
        integerQSlider.setStyleSheet("QWidget { background-color: #ffffb8 }")
        integerQSlider.setRange(1, 1000)
        integerQSlider.setSingleStep(1)
        integerQSlider.setValue(250)
        integerQSlider.valueChanged.connect(update_label)

        integerQLabel = QLabel()
        integerQLabel.setFont(QFont('Serif', 20))
        integerQLabel.setAlignment(Qt.AlignCenter)
        integerQLabel.setStyleSheet("QWidget { background-color: #ffffb8 }")

        unitQSlider = QSlider(Qt.Horizontal)
        unitQSlider.setFocusPolicy(Qt.NoFocus)
        unitQSlider.setMinimumSize(1, 100)
        unitQSlider.setStyleSheet("QWidget { background-color: #ffffb8 }")
        unitQSlider.setRange(1, 5)
        unitQSlider.setValue(4)
        unitQSlider.valueChanged.connect(update_label)

        unitQLabel = QLabel()
        unitQLabel.setFont(QFont('Serif', 20))
        unitQLabel.setAlignment(Qt.AlignCenter)
        unitQLabel.setStyleSheet("QWidget { background-color: #ffffb8 }")

        frequencyQLabel = QLabel()
        frequencyQLabel.setFont(QFont('Serif', 20))
        frequencyQLabel.setMinimumSize(200, 1)
        frequencyQLabel.setMaximumSize(200, 500)
        frequencyQLabel.setAlignment(Qt.AlignCenter)
        frequencyQLabel.setStyleSheet("QWidget { background-color: #ffffb8 }")

        update_label()

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(integerQSlider, 1, 1, 1, 1)
        grid.addWidget(integerQLabel, 2, 1, 1, 1)
        grid.addWidget(unitQSlider, 1, 2, 1, 1)
        grid.addWidget(unitQLabel, 2, 2, 1, 1)
        grid.addWidget(frequencyQLabel, 1, 3, 2, 1)

        self.setLayout(grid)
        self.resize(1000, 200)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyFrequency()
    ex.show()
    print(ex.get_frequency())
    sys.exit(app.exec_())
