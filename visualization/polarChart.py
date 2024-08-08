from PyQt5.QtChart import QChart, QPolarChart, QScatterSeries, QValueAxis, QCategoryAxis, QChartView
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtGui import QPainter
from PyQt5 import QtWidgets

#문제 : 2,4가 안움직이는거 같음

class PolarChart:
    def __init__(self):
        self.x = 0
        self.chart = QPolarChart()
        self.chart.legend().hide()
        self.series1 = QScatterSeries()
        self.series2 = QScatterSeries()


        self.series1.append(0, 0)
        self.series1.append(120, 0)
        self.series1.append(240, 0)
        self.series1.append(360, 0)
        # self.series1.append(360, 0)


        self.chart.addSeries(self.series1)
        # self.chart.addSeries(self.series2)


        self.angularAxis = QCategoryAxis()
        self.angularAxis.setTickCount(9)
        self.angularAxis.setLabelFormat("%.1f")
        self.angularAxis.append("Sensor 1", 0)
        self.angularAxis.append("Sensor 2", 90)
        self.angularAxis.append("Sensor 3", 180)
        self.angularAxis.append("Sensor 4", 270)
        # self.angularAxis.append("Sensor 5", 288)

        self.chart.addAxis(self.angularAxis, QPolarChart.PolarOrientationAngular)

        self.radialAxis = QValueAxis()
        self.radialAxis.setTickCount(9)
        self.radialAxis.setLabelFormat("%d")
        self.radialAxis.setRange(0, 255)  # Adjust this range as necessary
        self.chart.addAxis(self.radialAxis, QPolarChart.PolarOrientationRadial)
        #
        # self.angularAxis2 = QCategoryAxis()
        # self.angularAxis2.setTickCount(8)
        # self.angularAxis2.setLabelFormat("%.1f")
        # self.angularAxis2.append("Sensor 2", 90)
        # self.chart.addAxis(self.angularAxis2, QPolarChart.PolarOrientationAngular)
        #
        # self.radialAxis2 = QValueAxis()
        # self.radialAxis2.setTickCount(9)
        # self.radialAxis2.setLabelFormat("%d")
        # self.radialAxis2.setRange(0, 255)  # Adjust this range as necessary
        # self.chart.addAxis(self.radialAxis2, QPolarChart.PolarOrientationRadial)

        self.series1.attachAxis(self.angularAxis)
        self.series1.attachAxis(self.radialAxis)

        # self.series2.attachAxis(self.angularAxis2)
        # self.series2.attachAxis(self.radialAxis2)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

    def get_views(self):
        return self.chart_view

    def update_chart_theme(self, theme):
        self.angularAxis.setTheme(theme)

    def update_polar_chart(self, sensorDataQueue):
        while not sensorDataQueue.empty():
            y1, y2, y3, y4 = sensorDataQueue.get_nowait()

            self.series1.replace(0,0, y1)
            self.series1.replace(1,90, y2)
            self.series1.replace(2,180, y3)
            self.series1.replace(3,270, y4)
            # self.series1.replace(4,360,y4)

            if self.series1.count() > 255:
                self.series1.remove(0)
                self.series2.remove(0)


    def update_chart_theme(self, theme):
        self.chart.setTheme(theme)
        # self.chart2.setTheme(theme)
        # self.chart3.setTheme(theme)
        # self.chart4.setTheme(theme)
