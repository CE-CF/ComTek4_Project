import WiFi.WiFi
import ImgProcess.Img_process as analysis
import multiprocessing as mp
import socket, time, struct, math, pickle
import numpy as np
import cv2


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

data = manager.Value(bytes, 0xff)
yaw = 0
pitch = 0
detected = True

heightShared = manager.Value(int, 0)
widthShared = manager.Value(int, 0)
xShared = manager.Value(int, 0)
yShared = manager.Value(int, 0)




##############################################################
# Functions
##############################################################


def Receiver(BUFFER_SIZE, number):
    while(1):
        try:
            x = net.Receive(BUFFER_SIZE)
            data = np.array(x,np.uint8)
            #data = x[0]
            #print(data)
            #data = pickle.loads(x)
            #print("pickle")
            analysis.drone_detection(data)
        except:
            print("Didn't receive anything")

def tcpSender(yaw, pitch, number):
    tal = 0
    while(1):
        time.sleep(1)
        packet = net.packer(-140, 140)
        print(packet)
        if detected == True:
            print("sending commands")
            net.Send(packet)
        else:
            print("Sending null commands")
            net.Send(packet)
            tal = tal + 1
            number.set(tal)

def imageProcessProcess():
    while(1):
        feed = data.get
        #Height, width, x, y = analysis.drone_detection(feed)
        analysis.drone_detection(feed)

##############################################################
# Main
##############################################################

if __name__ == '__main__':
    try:
        sendProcess = mp.Process(target=tcpSender, args=(yaw, pitch, number))
        #receiveProcess = mp.Process(target=Receiver, args=(2048,number))
        #imgProcessor = mp.Process(target=imageProcessProcess,)


        #receiveProcess.start()
        sendProcess.start()
        #imgProcessor.start()
        #receiveProcess.join()
        sendProcess.join()
        #imgProcessor.join()
    except KeyboardInterrupt:
        print("Shutting down....")
        sendProcess.terminate()
        #receiveProcess.terminate()
        print("Bye")
