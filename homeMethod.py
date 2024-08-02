import re
import threading
import serial
import sensorData
import serial.tools.list_ports as sp

def start_graph(main_instance):
    serialSensorReadThread = threading.Thread(target=sensorData.serialSensorRead, daemon=True)
    serialSensorReadThread.start()
    sensorData.startGraph()
    main_instance.timer.start(100)  # update every 100 ms

def end_graph(main_instance):
    main_instance.timer.stop()

def close_window(main_instance):
    main_instance.close()

def update_plot(main_instance):
    sensorData.animate()
    main_instance.canvas.draw()

def identify_port():
    ports = sp.comports()
    nlist = []
    for port in ports:
        number = re.sub(r'[^0-9]', '', port.device)
        nlist.append(number)
    return nlist

def combox_select(cb):
    cur_number = re.sub(r'[^0-9]', '', cb.currentText())
    return cur_number

def serialSensorRead():
    ser = serial.Serial(port='COM' + combox_select(), baudrate=9600)
    try:
        while True:
            serialData = ser.readline().decode().rstrip()
            values = serialData.split(",")
            if len(values) == 5:
                y1, y2, y3, y4, y5 = map(int, values)
                sensorData.sensorDataQueue.put((y1, y2, y3, y4))
    except Exception as e:
        print(f"Error reading serial data: {e}")
