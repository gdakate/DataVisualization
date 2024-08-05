import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QScatterSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QTimer
import threading
import serial
import queue
import os


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.sensorDataQueue = queue.Queue()
        self.x = 0
        self.max_points = 255
        self.setWindowTitle("Real-time Graph")
        self.setGeometry(600, 400, 800, 600)

        self.series1 = QLineSeries()
        self.series2 = QLineSeries()
        self.series3 = QLineSeries()
        self.series4 = QLineSeries()

        self.series1.setColor(Qt.darkGray)
        self.series2.setColor(Qt.blue)
        self.series3.setColor(Qt.yellow)
        self.series4.setColor(Qt.green)


        self.current_point_series1 = QScatterSeries()
        self.current_point_series2 = QScatterSeries()
        self.current_point_series3 = QScatterSeries()
        self.current_point_series4 = QScatterSeries()

        self.current_point_series1.setColor(Qt.red)
        self.current_point_series2.setColor(Qt.red)
        self.current_point_series3.setColor(Qt.red)
        self.current_point_series4.setColor(Qt.red)

        self.chart = QChart()
        self.chart2 = QChart()
        self.chart3 = QChart()
        self.chart4 = QChart()

        self.chart.legend().hide()
        self.chart2.legend().hide()
        self.chart3.legend().hide()
        self.chart4.legend().hide()


        self.chart.addSeries(self.series1)
        self.chart.addSeries(self.current_point_series1)
        self.chart2.addSeries(self.series2)
        self.chart2.addSeries(self.current_point_series2)
        self.chart3.addSeries(self.series3)
        self.chart3.addSeries(self.current_point_series3)
        self.chart4.addSeries(self.series4)
        self.chart4.addSeries(self.current_point_series4)

        self.chart.createDefaultAxes()
        self.chart2.createDefaultAxes()
        self.chart3.createDefaultAxes()
        self.chart4.createDefaultAxes()

        self.chart_view = QChartView(self.chart)
        self.chart_view2 = QChartView(self.chart2)
        self.chart_view3 = QChartView(self.chart3)
        self.chart_view4 = QChartView(self.chart4)

        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view2.setRenderHint(QPainter.Antialiasing)
        self.chart_view3.setRenderHint(QPainter.Antialiasing)
        self.chart_view4.setRenderHint(QPainter.Antialiasing)

        self.central_widget = QWidget()

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.chart_view)
        self.layout.addWidget(self.chart_view2)
        self.layout.addWidget(self.chart_view3)
        self.layout.addWidget(self.chart_view4)

        self.setCentralWidget(self.central_widget)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(1)  # 100 ms마다 업데이트

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

            self.current_point_series1.clear()
            self.current_point_series1.append(self.x, y1)
            self.current_point_series2.clear()
            self.current_point_series2.append(self.x, y2)
            self.current_point_series3.clear()
            self.current_point_series3.append(self.x, y3)
            self.current_point_series4.clear()
            self.current_point_series4.append(self.x, y4)

            self.x += 1

            if self.series1.count() > self.max_points:
                self.series1.remove(0)
                self.series2.remove(0)
                self.series3.remove(0)
                self.series4.remove(0)
            self.chart.axisX(self.series1).setRange(max(0, self.x - self.max_points), self.x)
            self.chart.axisY(self.series1).setRange(0, self.max_points)

            self.chart2.axisX(self.series2).setRange(max(0, self.x - self.max_points), self.x)
            self.chart2.axisY(self.series2).setRange(0, self.max_points)

            self.chart3.axisX(self.series3).setRange(max(0, self.x - self.max_points), self.x)
            self.chart3.axisY(self.series3).setRange(0, self.max_points)

            self.chart4.axisX(self.series4).setRange(max(0, self.x - self.max_points), self.x)
            self.chart4.axisY(self.series4).setRange(0, self.max_points)

    def start(self):
        self.serialSensorReadThread = threading.Thread(target=self.read_serial_sensor, daemon=True)
        self.serialSensorReadThread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.start()
    window.show()

    sys.exit(app.exec_())
