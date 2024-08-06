from PyQt5.QtChart import QChart, QLineSeries, QChartView, QValueAxis, QScatterSeries
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui

class LineGraph:
    def __init__(self):

        self.max_points = 255
        self.x =0


        # 선 그래프 객체 생성
        self.series1 = QLineSeries()
        self.series2 = QLineSeries()
        self.series3 = QLineSeries()
        self.series4 = QLineSeries()


        # 커서 객체 생성
        self.cursor_series1 = QScatterSeries()
        self.cursor_series2 = QScatterSeries()
        self.cursor_series3 = QScatterSeries()
        self.cursor_series4 = QScatterSeries()

        # 커서 설정
        self.cursor_series1.setMarkerSize(15)
        self.cursor_series2.setMarkerSize(15)
        self.cursor_series3.setMarkerSize(15)
        self.cursor_series4.setMarkerSize(15)

        # 차트 객체 생성
        self.chart1 = QChart()
        self.chart2 = QChart()
        self.chart3 = QChart()
        self.chart4 = QChart()

        # 차트 내 표기 숨기기
        self.chart1.legend().hide()
        self.chart2.legend().hide()
        self.chart3.legend().hide()
        self.chart4.legend().hide()

        self.chart1.addSeries(self.series1)
        self.chart1.addSeries(self.cursor_series1)
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
        self.chart1.addAxis(self.axis_x1, Qt.AlignBottom)
        self.chart1.addAxis(self.axis_y1, Qt.AlignLeft)
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

        self.chart_view1 = QChartView(self.chart1)
        self.chart_view2 = QChartView(self.chart2)
        self.chart_view3 = QChartView(self.chart3)
        self.chart_view4 = QChartView(self.chart4)

        self.chart_view1.setRenderHint(QPainter.Antialiasing)
        self.chart_view2.setRenderHint(QPainter.Antialiasing)
        self.chart_view3.setRenderHint(QPainter.Antialiasing)
        self.chart_view4.setRenderHint(QPainter.Antialiasing)

        self.set_size_policy(self.chart_view1)
        self.set_size_policy(self.chart_view2)
        self.set_size_policy(self.chart_view3)
        self.set_size_policy(self.chart_view4)

    def update_chart(self,sensorDataQueue):
        while not sensorDataQueue.empty():
            y1, y2, y3, y4 = sensorDataQueue.get_nowait()

            self.series1.append(self.x, y1)
            self.series2.append(self.x, y2)
            self.series3.append(self.x, y3)
            self.series4.append(self.x, y4)

            self.cursor_series1.clear()
            self.cursor_series2.clear()
            self.cursor_series3.clear()
            self.cursor_series4.clear()

            if self.series1.count() > 255:
                self.series1.remove(0)
                self.series2.remove(0)
                self.series3.remove(0)
                self.series4.remove(0)

            left_range = (self.x // self.max_points) * self.max_points
            self.cursor_series1.append(left_range + self.x % self.max_points, y1)
            self.cursor_series2.append(left_range + self.x % self.max_points, y2)
            self.cursor_series3.append(left_range + self.x % self.max_points, y3)
            self.cursor_series4.append(left_range + self.x % self.max_points, y4)

            self.x += 1

            left_range = (self.x // self.max_points) * self.max_points
            right_range = left_range + self.max_points

            self.axis_x1.setRange(left_range, right_range)
            self.axis_x2.setRange(left_range, right_range)
            self.axis_x3.setRange(left_range, right_range)
            self.axis_x4.setRange(left_range, right_range)

        # Process UI events to update the chart
        QtWidgets.QApplication.processEvents()

    def set_size_policy(self, chart_view):
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        chart_view.setSizePolicy(size_policy)
        chart_view.setMinimumSize(400, 400)

    def get_views(self):
        return self.chart_view1, self.chart_view2, self.chart_view3, self.chart_view4

    def update_chart_theme(self, theme):
        self.chart1.setTheme(theme)
        self.chart2.setTheme(theme)
        self.chart3.setTheme(theme)
        self.chart4.setTheme(theme)