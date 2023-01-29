import base64
from time import sleep

import threading

import cv2
import socketio  # python-socketio by @miguelgrinberg

sio = socketio.Client()
connected = False


def startTransmission(camIndex, camName):
    print("Starting video transmission: " + camName)
    cam = cv2.VideoCapture(camIndex)
    while (connected):
        ret, frame = cam.read()                     # get frame from webcam
        # from image to binary buffer
        res, frame = cv2.imencode('.jpg', frame)
        data = base64.b64encode(frame)
        try:
            sio.emit(camName, data)
        except Exception:
            pass
    cam.release()


@sio.event
def connect():
    global connected
    connected = True
    sio.emit('name', b'video')
    print("I'm connected!")

    cam0 = threading.Thread(target=startTransmission, args=(0, "data1"))
    cam1 = threading.Thread(target=startTransmission, args=(1, "data2"))
    cam2 = threading.Thread(target=startTransmission, args=(2, "data3"))

    cam0.start()
    cam1.start()
    cam2.start()


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")
    global connected
    connected = False


sio.connect('http://127.0.0.1:3000')