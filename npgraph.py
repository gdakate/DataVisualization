import queue
import numpy as np
import serial
import tkinter as tk
import threading
import time


sensorDataQueue = queue.Queue()

# 데이터 배열 초기화
data = np.zeros(255)
cursor_position = 0

# 시리얼 포트 초기화 (포트를 실제 사용 중인 포트로 변경하세요)
ser = serial.Serial(port='COM6', baudrate=9600)

# 데이터 업데이트 함수
def update_data():
    global data, cursor_position
    cursor_position = (cursor_position + 1) % 255
    y1, y2, y3, y4 = getAllSensorDataOnQueue()
    if y1:  # y1 리스트가 비어 있지 않은 경우에만 업데이트
        print(y1[0])
        data[cursor_position] = y1[0]

# 그래프 그리기 함수
def draw_graph(canvas):
    canvas.delete("all")
    width = canvas.winfo_width() // 2  # 가로 길이를 절반으로 줄임
    height = canvas.winfo_height() // 4  # 높이의 1/4로 제한
    max_value = np.max(data)

    if max_value == 0:
        max_value = 1

    for i in range(255):
        x = int(i * (width / 255))
        y = height - int((data[i] / max_value) * height)
        if i== cursor_position:
            canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="red", outline="red")
        else:
            canvas.create_oval(x - 0.5, y - 0.5, x + 0.5, y + 0.5, fill="black", outline="black")


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

# 데이터 수신 및 그래프 업데이트 함수
def serial_data_reader():
    global data, cursor_position
    try:
        while True:
            serialData = ser.readline().decode().rstrip()
            values = serialData.split(",")
            if len(values) == 5:
                y1, y2, y3, y4, y5 = map(int, values)
                sensorDataQueue.put((y1, y2, y3, y4))

            update_data()
            draw_graph(canvas)
            time.sleep(0.002)  # 속도를 조절


    except Exception as e:
        print(f"Error reading serial data: {e}")
    finally:
        ser.close()

# tkinter GUI 설정
root = tk.Tk()
root.title("Real-time Graph")

label = tk.Label(root, text=f"현재 커서 위치 {cursor_position}")
label.pack()

canvas = tk.Canvas(root, width=800, height=400, bg="white")
canvas.pack()

# 시리얼 데이터 읽기 스레드 시작
thread = threading.Thread(target=serial_data_reader)
thread.daemon = True
thread.start()

root.mainloop()
