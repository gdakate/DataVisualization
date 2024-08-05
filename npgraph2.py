import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QValueAxis, QScatterSeries
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QTimer
import threading
import serial
import queue


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.sensorDataQueue = queue.Queue()
        self.x = 0
        self.max_points = 255
        self.setWindowTitle("Real-time Graph")
        self.setGeometry(100, 100, 1200, 800)  # 전체 윈도우 크기 설정

        self.series1 = QLineSeries()
        self.series2 = QLineSeries()
        self.series3 = QLineSeries()
        self.series4 = QLineSeries()
        self.cursor_series1 = QScatterSeries()

        pen1 = QPen(Qt.magenta)
        pen1.setWidth(3)
        self.series1.setPen(pen1)

        pen2 = QPen(Qt.blue)
        pen2.setWidth(3)
        self.series2.setPen(pen2)

        pen3 = QPen(Qt.darkMagenta)
        pen3.setWidth(3)
        self.series3.setPen(pen3)

        pen4 = QPen(Qt.darkGreen)
        pen4.setWidth(3)
        self.series4.setPen(pen4)

        self.cursor_series1.setColor(Qt.red)
        self.cursor_series1.setMarkerSize(15)  # 커서 크기를 15로 설정

        self.chart = QChart()
        self.chart2 = QChart()
        self.chart3 = QChart()
        self.chart4 = QChart()

        self.chart.legend().hide()
        self.chart2.legend().hide()
        self.chart3.legend().hide()
        self.chart4.legend().hide()

        self.chart.addSeries(self.series1)
        self.chart.addSeries(self.cursor_series1)
        self.chart2.addSeries(self.series2)
        self.chart3.addSeries(self.series3)
        self.chart4.addSeries(self.series4)

        self.axis_x1 = QValueAxis()
        self.axis_x1.setRange(0, self.max_points)
        self.axis_y1 = QValueAxis()
        self.axis_y1.setRange(0, 300)
        self.chart.addAxis(self.axis_x1, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y1, Qt.AlignLeft)
        self.series1.attachAxis(self.axis_x1)
        self.series1.attachAxis(self.axis_y1)
        self.cursor_series1.attachAxis(self.axis_x1)
        self.cursor_series1.attachAxis(self.axis_y1)

        self.axis_x2 = QValueAxis()
        self.axis_x2.setRange(0, self.max_points)
        self.axis_y2 = QValueAxis()
        self.axis_y2.setRange(0, 300)
        self.chart2.addAxis(self.axis_x2, Qt.AlignBottom)
        self.chart2.addAxis(self.axis_y2, Qt.AlignLeft)
        self.series2.attachAxis(self.axis_x2)
        self.series2.attachAxis(self.axis_y2)

        self.axis_x3 = QValueAxis()
        self.axis_x3.setRange(0, self.max_points)
        self.axis_y3 = QValueAxis()
        self.axis_y3.setRange(0, 300)
        self.chart3.addAxis(self.axis_x3, Qt.AlignBottom)
        self.chart3.addAxis(self.axis_y3, Qt.AlignLeft)
        self.series3.attachAxis(self.axis_x3)
        self.series3.attachAxis(self.axis_y3)

        self.axis_x4 = QValueAxis()
        self.axis_x4.setRange(0, self.max_points)
        self.axis_y4 = QValueAxis()
        self.axis_y4.setRange(0, 300)
        self.chart4.addAxis(self.axis_x4, Qt.AlignBottom)
        self.chart4.addAxis(self.axis_y4, Qt.AlignLeft)
        self.series4.attachAxis(self.axis_x4)
        self.series4.attachAxis(self.axis_y4)

        self.chart_view = QChartView(self.chart)
        self.chart_view2 = QChartView(self.chart2)
        self.chart_view3 = QChartView(self.chart3)
        self.chart_view4 = QChartView(self.chart4)

        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view2.setRenderHint(QPainter.Antialiasing)
        self.chart_view3.setRenderHint(QPainter.Antialiasing)
        self.chart_view4.setRenderHint(QPainter.Antialiasing)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.start_button = QPushButton("START")
        self.start_button.clicked.connect(self.start)

        self.stop_button = QPushButton("STOP")
        self.stop_button.clicked.connect(self.stop)

        # h_layout = QHBoxLayout(self.central_widget)
        # h_layout.addWidget(self.start_button)
        # h_layout.addWidget(self.stop_button)

        v_layout = QVBoxLayout(self.central_widget)
        # v_layout.addLayout(h_layout)
        v_layout.addWidget(self.chart_view)
        v_layout.addWidget(self.chart_view2)
        v_layout.addWidget(self.chart_view3)
        v_layout.addWidget(self.chart_view4)


        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(1)

    def read_serial_sensor(self):
        self.ser = serial.Serial(port='COM6', baudrate=9600)
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

    def update_chart(self):
        while not self.sensorDataQueue.empty():
            y1, y2, y3, y4 = self.sensorDataQueue.get_nowait()

            self.series1.append(self.x, y1)
            self.series2.append(self.x, y2)
            self.series3.append(self.x, y3)
            self.series4.append(self.x, y4)

            self.cursor_series1.clear()
            self.cursor_series1.append(self.x % self.max_points, y1)

            self.x += 1

            left_range = (self.x // self.max_points) * self.max_points
            right_range = left_range + self.max_points

            self.axis_x1.setRange(left_range, right_range)
            self.axis_x2.setRange(left_range, right_range)
            self.axis_x3.setRange(left_range, right_range)
            self.axis_x4.setRange(left_range, right_range)

    def start(self):
        self.serialSensorReadThread = threading.Thread(target=self.read_serial_sensor, daemon=True)
        self.serialSensorReadThread.start()

    def stop(self):
        self.timer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    window.start()
    sys.exit(app.exec_())
