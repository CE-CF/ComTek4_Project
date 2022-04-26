import WiFi.WiFi
import multiprocessing
import socket
import time
import struct
import numpy as np
import math

net = WiFi.WiFi

data = b''

yawAngle = 0
yawSpeed = 0
pitchAngle = 0 
pitchSpeed = 0


def packer():
    struct.pack(h, yawAngle, pitchangle)
    struct.pack(B, yawSpeed,pitchSpeed)


def Receiver(BUFFER_SIZE):
    while(1):
        try:
            data = net.Receive(BUFFER_SIZE)
        except:
            print("Didn't receive anything")
        print(data)   

def Sender(commands):
    while(1):
        print("sending commands")
        net.Send(commands)

def tcpSender(commands):
    while(1):
        print("sending commands")
        net.tcpSend(commands)


if __name__ == '__main__':
    sendProcess = multiprocessing.Process(target=Sender, args=(commands,))
    receiveProcess = multiprocessing.Process(target=Receiver, args=(2048,))

    receiveProcess.start()
    sendProcess.start()
