from PyQt5.QtChart import QBarSet, QChart, QBarSeries, QBarCategoryAxis, QValueAxis, QChartView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter


class BarChart:
    def __init__(self):
        self.bar_set = QBarSet('')
        self.bar_set.append([0, 0, 0, 0])  # Initialize with zero values
        self.bar_series = QBarSeries()
        self.bar_series.append(self.bar_set)

        self.chart = QChart()
        self.chart.addSeries(self.bar_series)
        self.chart.setTitle("Bar Chart")

        self.categories = ['sensor 1', 'sensor 2', 'sensor 3', 'sensor 4']

        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(self.categories)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.bar_series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.bar_series.attachAxis(self.axis_y)
        self.axis_y.setRange(0, 255)

        self.chart.legend().hide()
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

    def get_view(self):
        return self.chart_view

    def update_bar_chart(self, sensorDataQueue):
        while not sensorDataQueue.empty():
            y1, y2, y3, y4 = sensorDataQueue.get_nowait()
            self.bar_set.replace(0, y1)
            self.bar_set.replace(1, y2)
            self.bar_set.replace(2, y3)
            self.bar_set.replace(3, y4)

    def update_chart_theme(self, theme):
        self.chart.setTheme(theme)
