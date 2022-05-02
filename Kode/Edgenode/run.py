import WiFi.WiFi
import multiprocessing as mp
import socket
import time
import struct
import numpy as np
import math


manager = mp.Manager()
net = WiFi.WiFi

number = manager.Value('H', 0)

coordlist = manger.list(0,0,0,0)

data = b''
yaw = 0
pitch = 0


detected = False




def Receiver(BUFFER_SIZE,number):
    while(1):
        try:
            data = net.Receive(BUFFER_SIZE)
            print(data)
        except:
            print("Didn't receive anything")
            print(number.get())



def tcpSender(yawAngle,pitchAngle,yawSpeed,pitchSpeed, number):
    tal = 0
    while(1):
        time.sleep(1)
        packet = net.packer(yaw, pitch)
        if detected == True:
            print("sending commands")
            net.Send(packet)
        else:
            print("Sending null commands")
            net.Send(packet)
            tal = tal + 1
            number.set(tal)

            





if __name__ == '__main__':
    try:
        sendProcess = mp.Process(target=tcpSender, args=(yawAngle, pitchAngle, yawSpeed, pitchSpeed, number))
        receiveProcess = mp.Process(target=Receiver, args=(2048,number))

        receiveProcess.start()
        sendProcess.start()
        receiveProcess.join()
        sendProcess.join()
    except KeyboardInterrupt:
        print("Shutting down....")
        sendProcess.terminate()
        receiveProcess.terminate()
        print("Bye")       
