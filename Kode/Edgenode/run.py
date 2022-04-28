import WiFi.WiFi
import multiprocessing
import socket
import time
import struct
import numpy as np
import math

net = WiFi.WiFi

data = b''

yawAngle = 180
yawSpeed = 2
pitchAngle = 180
pitchSpeed = 3

CTS = False

def packer(yawAngle,pitchAngle,yawSpeed,pitchSpeed):
    fullPack = struct.pack('hBhB', yawAngle, yawSpeed, pitchAngle,pitchSpeed)

    return fullPack




def Receiver(BUFFER_SIZE):
    while(1):
        try:
            data = net.Receive(BUFFER_SIZE)
            print(data)
        except:
            print("Didn't receive anything")

def tcpSender(yawAngle,pitchAngle,yawSpeed,pitchSpeed):
    while(1):
        time.sleep(1)
        packet = packer(yawAngle, pitchAngle, yawSpeed, pitchSpeed)
        if CTS == True:
            print("sending commands")
            net.Send(packet)
        else:
            print("Sending null commands")
            net.Send(packet)
            


if __name__ == '__main__':
    try:
        sendProcess = multiprocessing.Process(target=tcpSender, args=(yawAngle, pitchAngle, yawSpeed, pitchSpeed))
        receiveProcess = multiprocessing.Process(target=Receiver, args=(2048,))

        receiveProcess.start()
        sendProcess.start()
        receiveProcess.join()
        sendProcess.join()
    except KeyboardInterrupt:
        print("Shutting down....")
        sendProcess.terminate()
        receiveProcess.terminate()
        print("Bye")


        
