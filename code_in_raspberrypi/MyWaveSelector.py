from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QGridLayout, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import sys


class MyWaveSelector(QWidget):
    updateBW = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.initUI()

    def get_wave_type(self):
        return self.fff

    def initUI(self):

        def update_label(integer):
            self.fff = integer
            self.updateBW.emit(self.fff)

        waveQLabel = QLabel('波形预览')
        waveQLabel.setFont(QFont('Serif', 30))
        waveQLabel.setAlignment(Qt.AlignCenter)
        waveQLabel.setMinimumSize(200, 1)
        waveQLabel.setMaximumSize(200, 500)
        waveQLabel.setStyleSheet("QWidget { background-color: #ffffb8 }")

        WaveQComoBox = QComboBox(self)
        WaveQComoBox.addItem("正弦波")
        WaveQComoBox.addItem("三角波")
        WaveQComoBox.addItem("下扫频")
        WaveQComoBox.addItem("上扫频")
        WaveQComoBox.setCurrentIndex(2)
        WaveQComoBox.setFont(QFont('Serif', 30))
        WaveQComoBox.setMinimumSize(1, 100)
        WaveQComoBox.setMaximumSize(1000, 100)
        WaveQComoBox.setStyleSheet("QWidget { background-color: #ffffb8 }")
        WaveQComoBox.activated[int].connect(update_label)

        update_label(2)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(waveQLabel, 1, 1, 1, 1)
        grid.addWidget(WaveQComoBox, 1, 2, 1, 1)
        self.setLayout(grid)
        self.resize(1000, 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWaveSelector()
    ex.show()
    print(ex.get_wave_type())
    sys.exit(app.exec_())
