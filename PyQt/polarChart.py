from PyQt5.QtChart import QChart, QPolarChart, QScatterSeries, QValueAxis, QCategoryAxis, QChartView
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtGui import QPainter
from PyQt5 import QtWidgets

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

        self.chart.addSeries(self.series1)

        self.angularAxis = QCategoryAxis()
        self.angularAxis.setTickCount(10)
        self.angularAxis.setLabelFormat("%.1f")
        self.angularAxis.append("Sensor 1", 0)
        self.angularAxis.append("Sensor 2", 90)
        self.angularAxis.append("Sensor 3", 180)
        self.angularAxis.append("Sensor 4", 270)
        self.angularAxis.append("Sensor 5", 360)
        self.angularAxis.append("Sensor 1", 45)
        self.angularAxis.append("Sensor 2", 135)
        self.angularAxis.append("Sensor 3", 225)
        # self.angularAxis.append("Sensor 4", 270)
        self.angularAxis.append("Sensor 5", 315)

        self.chart.addAxis(self.angularAxis, QPolarChart.PolarOrientationAngular)

        self.radialAxis = QValueAxis()
        self.radialAxis.setTickCount(5)
        self.radialAxis.setLabelFormat("%d")
        self.radialAxis.setRange(0, 255)
        self.chart.addAxis(self.radialAxis, QPolarChart.PolarOrientationRadial)

        self.series1.attachAxis(self.angularAxis)
        self.series1.attachAxis(self.radialAxis)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

    def get_view(self):
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

            if self.series1.count() > 255:
                self.series1.remove(0)
                self.series2.remove(0)


    def update_chart_theme(self, theme):
        self.chart.setTheme(theme)
