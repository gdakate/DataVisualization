import re
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtChart import *
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QComboBox, \
    QGridLayout
from PyQt5.QtGui import QIcon
import threading
import serial
import queue
import serial.tools.list_ports as sp

from visualization.barChart import BarChart
from visualization.graphLine1 import LineGraph
from visualization.polarChart import PolarChart


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.sensorDataQueue = queue.Queue()

        #윈도우 설정
        self.setWindowTitle("Real-time Graph")
        self.setGeometry(70, 70, 1500, 800)

        #콤보박스
        self.cb = QComboBox(self)
        self.numberlist = self.identify_port()
        for i in self.numberlist:
            self.cb.addItem("COM " + str(i))
        self.cb.setMinimumSize(10, 25)
        self.combox_select()

        #버튼 생성,설정
        self.start_button = QPushButton("START")
        # self.start_button.setIcon(QIcon("image/play.png"))
        self.start_button.clicked.connect(self.start)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon("image/stop-button.png"))
        self.stop_button.clicked.connect(self.stop)

        self.line_button = QPushButton("LINE")
        self.line_button.clicked.connect(self.show_line_graph)

        self.bar_button = QPushButton("BAR")
        self.bar_button.clicked.connect(self.show_bar_graph)

        self.polar_button = QPushButton("POLAR")
        self.polar_button.clicked.connect(self.show_polar_graph)

        # QT 테마 적용
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Light", QChart.ChartThemeLight)
        self.theme_combo.addItem("Blue Cerulean", QChart.ChartThemeBlueCerulean)
        self.theme_combo.addItem("Dark", QChart.ChartThemeDark)
        self.theme_combo.addItem("Brown Sand", QChart.ChartThemeBrownSand)
        self.theme_combo.addItem("Blue NCS", QChart.ChartThemeBlueNcs)
        self.theme_combo.addItem("High Contrast", QChart.ChartThemeHighContrast)
        self.theme_combo.addItem("Blue Icy", QChart.ChartThemeBlueIcy)
        self.theme_combo.addItem("Qt", QChart.ChartThemeQt)

        self.theme_combo.currentIndexChanged.connect(self.choose_graph_theme)

        #레이아웃 설정
        self.central_widget = QWidget()
        self.menu_widget = QWidget()
        self.setMenuWidget(self.menu_widget)
        self.setCentralWidget(self.central_widget)

        self.v_layout = QGridLayout(self.central_widget)

        self.h_layout = QHBoxLayout(self.menu_widget)
        self.h_layout.addWidget(self.cb)
        self.h_layout.addWidget(self.start_button)
        self.h_layout.addWidget(self.stop_button)
        self.h_layout.addWidget(self.line_button)
        self.h_layout.addWidget(self.bar_button)
        self.h_layout.addWidget(self.polar_button)
        self.h_layout.addWidget(self.theme_combo)

        self.line_graph = None
        self.polar_graph = None
        self.bar_graph = None

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.choose_graph)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def choose_graph(self):
        if self.line_graph:
            self.line_graph.update_chart(self.sensorDataQueue)
        elif self.polar_graph:
            self.polar_graph.update_polar_chart(self.sensorDataQueue)
        elif self.bar_graph:
            self.bar_graph.update_bar_chart(self.sensorDataQueue)

    def choose_graph_theme(self):
        theme = self.theme_combo.currentData()
        if self.line_graph:
            self.line_graph.update_chart_theme(theme)
        elif self.polar_graph:
            self.polar_graph.update_chart_theme(theme)
        elif self.bar_graph:
            self.bar_graph.update_chart_theme(theme)

    def show_line_graph(self):
        self.clear_layout(self.v_layout)
        self.line_graph = LineGraph()
        self.polar_graph = None
        self.bar_graph = None
        self.choose_graph_theme()

        view1,view2,view3,view4 = self.line_graph.get_views()
        self.v_layout.addWidget(view1,0,0)
        self.v_layout.addWidget(view2,0,1)
        self.v_layout.addWidget(view3,1,0)
        self.v_layout.addWidget(view4,1,1)

    def show_bar_graph(self):
        self.clear_layout(self.v_layout)
        self.bar_graph = BarChart()
        self.line_graph = None
        self.polar_graph = None
        self.choose_graph_theme()

        view = self.bar_graph.get_view()
        self.v_layout.addWidget(view,0,0)

    def show_polar_graph(self):
        self.clear_layout(self.v_layout)
        self.polar_graph = PolarChart()
        self.line_graph = None
        self.bar_graph = None
        self.choose_graph_theme()

        view = self.polar_graph.get_view()
        self.v_layout.addWidget(view,0,0)

    def read_serial_sensor(self):
        self.ser = serial.Serial(port='COM' + self.combox_select(), baudrate=9600)
        try:
            while True:
                serialData = self.ser.readline().decode().rstrip()
                values = serialData.split(",")
                if len(values) == 5:
                    y1, y2, y3, y4, y5 = map(int, values)
                    self.sensorDataQueue.put((y1, y2, y3, y4))
                    print(y1, y2, y3, y4)
        except Exception as e:
            print(f"Error reading serial data: {e}")

    def start(self):
        self.serialSensorReadThread = threading.Thread(target=self.read_serial_sensor, daemon=True)
        self.serialSensorReadThread.start()
        # self.start_button.setIcon(QIcon("image/play-button.png"))
        self.timer.start(1)
    def stop(self):
        if self.line_graph:
            self.timer.stop()

    def identify_port(self):
        self.ports = sp.comports()
        self.nlist = []
        for port in self.ports:
            self.number = re.sub(r'[^0-9]', '', port.device)
            self.nlist.append(self.number)
        return self.nlist

    def combox_select(self):
        self.cur_number = re.sub(r'[^0-9]', '', self.cb.currentText())
        return self.cur_number

    def restart(self):
        self.serialSensorReadThread = threading.Thread(target=self.read_serial_sensor, daemon=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
