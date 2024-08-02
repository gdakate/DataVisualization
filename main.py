import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import sensorData
import homeMethod

class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.paused = False
        self.label = QLabel("Graph")

        self.fig = sensorData.getFig()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # buttons
        self.startButton = QPushButton("START")
        self.startButton.clicked.connect(lambda: homeMethod.start_graph(self))
        self.startButton.setMinimumSize(300, 50)
        self.startButton.setStyleSheet("font-size:15px; font-family:Arial;")

        self.endButton = QPushButton("END")
        self.endButton.clicked.connect(lambda: homeMethod.end_graph(self))
        self.endButton.setMinimumSize(300, 50)
        self.endButton.setStyleSheet("font-size:15px; font-family:Arial;")

        self.closeButton = QPushButton("CLOSE")
        self.closeButton.clicked.connect(lambda: homeMethod.close_window(self))
        self.closeButton.setMinimumSize(50, 50)
        self.closeButton.setStyleSheet("font-size:15px; font-family:Arial;")

        # COM port 설정
        self.combo_label = QLabel("연결 COM 포트")
        self.combo_label.setMinimumSize(70, 10)
        self.cb = QComboBox(self)
        numberlist = homeMethod.identify_port()
        for i in numberlist:
            self.cb.addItem("COM " + str(i))
        self.cb.setMinimumSize(10, 25)
        homeMethod.combox_select(self.cb)

        buttons = QHBoxLayout()
        buttons.addWidget(self.startButton)
        buttons.addWidget(self.endButton)
        buttons.addWidget(self.closeButton)

        combo = QHBoxLayout()
        combo.addWidget(self.combo_label)
        combo.addWidget(self.cb)

        box = QVBoxLayout()
        box.addLayout(combo)
        box.addWidget(self.toolbar)
        box.addWidget(self.canvas)
        box.addLayout(buttons)
        self.setLayout(box)
        self.setGeometry(600, 100, 1000, 500)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: homeMethod.update_plot(self))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

