
import matplotlib.pyplot as plt
import numpy as np
import serial
import matplotlib.animation as animation
import queue
import threading

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sensorDataQueue = queue.Queue()


def serialSensorRead():
    # ser = get_serial_port()
    ser = serial.Serial(port='COM6', baudrate=9600)

    try:
        while True:
            seiralData = ser.readline().decode().rstrip()
            y1, y2, y3, y4, y5 = seiralData.split(",")
            y1 = int(y1)
            y2 = int(y2)
            y3 = int(y3)
            y4 = int(y4)
            y5 = int(y5)
            print(y1, y2, y3, y4, y5)

            sensorDataQueue.put((y1, y2, y3, y4))

    except Exception as e:
        print(f"Error reading serial data: {e}")


def get_serial_port():
    ser = serial.Serial(port='COM6', baudrate=9600)
    return ser



def subplot_setting(fig, number,color):
    test = fig.add_subplot(4, 1, number, xlim=(0, 100), ylim=(0, 300))
    line_y, = test.plot([], [], lw=2, color=color)
    line_y, = test.plot(np.arange(100), np.ones(100, dtype=np.float64) * np.nan, lw=2, color="red", label="y1")
    test.xaxis.set_visible(False)
    test.yaxis.set_visible(False)
    return line_y

#general setting
fig = plt.figure()
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0, hspace=0)
line_y1 = subplot_setting(fig, 1,"red")
line_y2 = subplot_setting(fig, 2,"green")
line_y3 = subplot_setting(fig, 3,"blue")
line_y4 = subplot_setting(fig, 4,"purple")
Xdata = list(np.arange(1000))


def init():
    line_y1.set_ydata(np.ones(100) * np.nan)
    line_y2.set_ydata(np.ones(100) * np.nan)
    line_y3.set_ydata(np.ones(100) * np.nan)
    line_y4.set_ydata(np.ones(100) * np.nan)
    return line_y1, line_y2, line_y3, line_y4


def getAllSensorDataOnQueue():
    y1Bunch = []
    y2Bunch = []
    y3Bunch = []
    y4Bunch = []

    while not sensorDataQueue.empty():
        y1, y2, y3, y4 = sensorDataQueue.get_nowait()
        y1Bunch.append(y1)
        y2Bunch.append(y2)
        y3Bunch.append(y3)
        y4Bunch.append(y4)
    return tuple(y1Bunch), tuple(y2Bunch), tuple(y3Bunch), tuple(y4Bunch)


# 그래프 업데이트
def animate():
    y1, y2, y3, y4 = getAllSensorDataOnQueue()
    if (y2.count == 0):
        return

    old_line_y1 = line_y1.get_ydata()
    new_line_y1 = np.concatenate([old_line_y1[len(y1):], y1])
    line_y1.set_ydata(new_line_y1)
    line_y1.set_color("red")


    old_line_y2 = line_y2.get_ydata()
    new_line_y2 = np.concatenate([old_line_y2[len(y2):], y2])
    line_y2.set_ydata(new_line_y2)
    line_y2.set_color("green")

    old_line_y3 = line_y3.get_ydata()
    new_line_y3 = np.concatenate([old_line_y3[len(y3):], y3])
    line_y3.set_ydata(new_line_y3)
    line_y3.set_color("blue")

    old_line_y4 = line_y4.get_ydata()
    new_line_y4 = np.concatenate([old_line_y4[len(y4):], y4])
    line_y4.set_ydata(new_line_y4)
    line_y4.set_color("yellow")

    return line_y1, line_y2, line_y3, line_y4


def getFig():
    return fig


def startGraph():
    anim =animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=False)

def startSerial():
    serialSensorReadThread = threading.Thread(target=serialSensorRead, daemon=True)
    serialSensorReadThread.start()

# def endGraph():
