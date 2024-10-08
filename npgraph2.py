import re
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QComboBox
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QValueAxis, QScatterSeries
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer, QSize
import threading
import serial
import queue
import serial.tools.list_ports as sp

# y축 높이 높게 -> 차이 잘 보이도록

class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.sensorDataQueue = queue.Queue()
        self.x = 0
        self.max_points = 255
        # 윈도우 설정
        self.setWindowTitle("Real-time Graph")
        self.setGeometry(70, 70, 1500, 800)

        # window 배경 이미지 설정
        self.image = QImage("image/pexels-photo-4504714.jpeg")
        self.simage = self.image.scaled(QSize(1500,800))
        self.palette = QPalette()
        self.palette.setBrush(10,QBrush(self.simage))
        self.setPalette(self.palette)

        # 선 그래프 객체 생성
        self.series1 = QLineSeries()
        self.series2 = QLineSeries()
        self.series3 = QLineSeries()
        self.series4 = QLineSeries()

        # 그래프 line 색상, 너비 설정
        pen1 = QPen(QtGui.QColor("#ffffe0"))
        pen1.setWidth(2)
        self.series1.setPen(pen1)
        pen2 = QPen(QtGui.QColor("#e0ffff"))
        pen2.setWidth(2)
        self.series2.setPen(pen2)
        pen3 = QPen(QtGui.QColor("#fff5ee"))
        pen3.setWidth(2)
        self.series3.setPen(pen3)
        pen4 = QPen(QtGui.QColor('#f0ffff'))
        pen4.setWidth(2)
        self.series4.setPen(pen4)

        # 커서 객체 생성
        self.cursor_series1 = QScatterSeries()
        self.cursor_series2 = QScatterSeries()
        self.cursor_series3 = QScatterSeries()
        self.cursor_series4 = QScatterSeries()

        # 커서 설정
        self.cursor_series1.setColor(QtGui.QColor("#ffd700"))
        self.cursor_series1.setMarkerSize(15)
        self.cursor_series2.setColor(QtGui.QColor("#afeeee"))
        self.cursor_series2.setMarkerSize(15)
        self.cursor_series3.setColor(QtGui.QColor("#f4a460"))
        self.cursor_series3.setMarkerSize(15)
        self.cursor_series4.setColor(QtGui.QColor("#afeeee"))
        self.cursor_series4.setMarkerSize(15)

        # 차트 객체 생성
        self.chart = QChart()
        self.chart2 = QChart()
        self.chart3 = QChart()
        self.chart4 = QChart()

        # 차트 내 표기 숨기기
        self.chart.legend().hide()
        self.chart2.legend().hide()
        self.chart3.legend().hide()
        self.chart4.legend().hide()

        self.chart.addSeries(self.series1)
        self.chart.addSeries(self.cursor_series1)
        self.chart2.addSeries(self.series2)
        self.chart2.addSeries(self.cursor_series2)
        self.chart3.addSeries(self.series3)
        self.chart3.addSeries(self.cursor_series3)
        self.chart4.addSeries(self.series4)
        self.chart4.addSeries(self.cursor_series4)

        # x축 y축 설정
        self.axis_x1 = QValueAxis()
        self.axis_x1.setRange(0, self.max_points)
        self.axis_y1 = QValueAxis()
        self.axis_y1.setRange(0, 500)
        self.chart.addAxis(self.axis_x1, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y1, Qt.AlignLeft)
        self.series1.attachAxis(self.axis_x1)
        self.series1.attachAxis(self.axis_y1)
        self.cursor_series1.attachAxis(self.axis_x1)
        self.cursor_series1.attachAxis(self.axis_y1)

        self.axis_x2 = QValueAxis()
        self.axis_x2.setRange(0, self.max_points)
        self.axis_y2 = QValueAxis()
        self.axis_y2.setRange(0, 255)
        self.chart2.addAxis(self.axis_x2, Qt.AlignBottom)
        self.chart2.addAxis(self.axis_y2, Qt.AlignLeft)
        self.series2.attachAxis(self.axis_x2)
        self.series2.attachAxis(self.axis_y2)
        self.cursor_series2.attachAxis(self.axis_x2)
        self.cursor_series2.attachAxis(self.axis_y2)

        self.axis_x3 = QValueAxis()
        self.axis_x3.setRange(0, self.max_points)
        self.axis_y3 = QValueAxis()
        self.axis_y3.setRange(0, 255)
        self.chart3.addAxis(self.axis_x3, Qt.AlignBottom)
        self.chart3.addAxis(self.axis_y3, Qt.AlignLeft)
        self.series3.attachAxis(self.axis_x3)
        self.series3.attachAxis(self.axis_y3)
        self.cursor_series3.attachAxis(self.axis_x3)
        self.cursor_series3.attachAxis(self.axis_y3)

        self.axis_x4 = QValueAxis()
        self.axis_x4.setRange(0, self.max_points)
        self.axis_y4 = QValueAxis()
        self.axis_y4.setRange(0, 255)
        self.chart4.addAxis(self.axis_x4, Qt.AlignBottom)
        self.chart4.addAxis(self.axis_y4, Qt.AlignLeft)
        self.series4.attachAxis(self.axis_x4)
        self.series4.attachAxis(self.axis_y4)
        self.cursor_series4.attachAxis(self.axis_x4)
        self.cursor_series4.attachAxis(self.axis_y4)


        self.chart_view = QChartView(self.chart)
        self.chart_view2 = QChartView(self.chart2)
        self.chart_view3 = QChartView(self.chart3)
        self.chart_view4 = QChartView(self.chart4)

        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view2.setRenderHint(QPainter.Antialiasing)
        self.chart_view3.setRenderHint(QPainter.Antialiasing)
        self.chart_view4.setRenderHint(QPainter.Antialiasing)

        # 콤보박스 생성 및 포트 번호 인식
        self.cb = QComboBox(self)
        self.numberlist = self.identify_port()
        for i in self.numberlist:
            self.cb.addItem("COM " + str(i))
        self.cb.setMinimumSize(10, 25)
        self.combox_select()

        #버튼 생성, 설정
        self.start_button = QPushButton()
        self.start_button.setIcon(QIcon("image/play.png"))
        self.start_button.clicked.connect(self.start)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon("image/stop-button.png"))
        self.stop_button.clicked.connect(self.stop)

        # self.close_button = QPushButton("CLOSE")
        # self.close_button.clicked.connect(self.close)

        # 위젯, 레이아웃 설정
        self.central_widget = QWidget()
        self.menu_widget = QWidget()
        self.setMenuWidget(self.menu_widget)
        self.setCentralWidget(self.central_widget)

        h_layout = QHBoxLayout(self.menu_widget)
        h_layout.addWidget(self.cb)
        h_layout.addWidget(self.start_button)
        h_layout.addWidget(self.stop_button)
        # h_layout.addWidget(self.close_button)

        v_layout = QVBoxLayout(self.central_widget)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.chart_view)
        v_layout.addWidget(self.chart_view2)
        v_layout.addWidget(self.chart_view3)
        v_layout.addWidget(self.chart_view4)

        # 그래프 x축 Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(1)

        # 그래프 x,y축, 배경 그리드 숨기기
        for chart_view in [self.chart_view, self.chart_view2, self.chart_view3, self.chart_view4]:
            chart_view.chart().axes(Qt.Horizontal)[0].setVisible(False)
            chart_view.chart().axes(Qt.Vertical)[0].setVisible(False)
            chart_view.chart().setBackgroundRoundness(0)
            chart_view.chart().setBackgroundVisible(False)
            for axis in chart_view.chart().axes():
                axis.setGridLineVisible(False)

    # 센서 읽고 데이터 가져오기
    def read_serial_sensor(self):
        self.ser = serial.Serial(port='COM'+self.combox_select(), baudrate=9600)
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
            self.cursor_series2.clear()
            self.cursor_series3.clear()
            self.cursor_series4.clear()

            # 과거 데이터 지워주기
            if self.series1.count() > 255:
                self.series1.remove(0)
                self.series2.remove(0)
                self.series3.remove(0)
                self.series4.remove(0)

            left_range = (self.x // self.max_points) * self.max_points
            self.cursor_series1.append(left_range+self.x % self.max_points, y1)
            self.cursor_series2.append(left_range+self.x % self.max_points, y2)
            self.cursor_series3.append(left_range+self.x % self.max_points, y3)
            self.cursor_series4.append(left_range+self.x % self.max_points, y4)

            self.x += 1

            # 255마다 x축 갱신
            left_range = (self.x // self.max_points) * self.max_points
            right_range = left_range + self.max_points

            self.axis_x1.setRange(left_range, right_range)
            self.axis_x2.setRange(left_range, right_range)
            self.axis_x3.setRange(left_range, right_range)
            self.axis_x4.setRange(left_range, right_range)


    def run(stop_event):
        while True:
            if stop_event.is_set():
                break
    def start(self):
        # self.run()
        self.serialSensorReadThread = threading.Thread(target=self.read_serial_sensor, daemon=True)
        self.serialSensorReadThread.start()
        self.start_button.setIcon(QIcon("image/play-button.png"))
        # self.start_button.setIconSize(QtCore.QSize(50,50))

    def stop(self):
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
    # window.start()
    sys.exit(app.exec_())
