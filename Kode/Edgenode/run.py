import WiFi.WiFi
import multiprocessing as mp
import socket
import time
import struct
import numpy as np
import math

##############################################################
# Renaming
##############################################################

net = WiFi.WiFi
manager = mp.Manager()

##############################################################
# Variables: Shared memory
##############################################################

number = manager.Value('H', 0)
coordlist = manager.list([0,0,0,0])

data = b''
yaw = 0
pitch = 0
detected = manager.Value(bool, False)

##############################################################
# Functions
##############################################################


def Receiver(BUFFER_SIZE,number):
    while(1):
        try:
            data = net.Receive(BUFFER_SIZE)
            print(data)
        except:
            print("Didn't receive anything")

def tcpSender(yaw, pitch, number):
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

##############################################################
# Main
##############################################################

if __name__ == '__main__':
    try:
        #sendProcess = mp.Process(target=tcpSender, args=(yaw, pitch, number))
        receiveProcess = mp.Process(target=Receiver, args=(2048,number))

        receiveProcess.start()
        #sendProcess.start()
        receiveProcess.join()
        #sendProcess.join()
    except KeyboardInterrupt:
        print("Shutting down....")
        #sendProcess.terminate()
        receiveProcess.terminate()
        print("Bye")       
