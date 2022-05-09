import WiFi.WiFi
import ImgProcess.Img_process as analysis
import McC.McC as correction
import multiprocessing as mp
import socket, time, struct, math
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
data = manager.Value(bytes, 0xff)
yaw = 0
pitch = 0
detected = manager.Value(bool, False)

heightShared = manager.Value(int, 0)
widthShared = manager.Value(int, 0)
xShared = manager.Value(int, 0)
yShared = manager.Value(int, 0)

Height = manager.Value(int, 0)
Width = manager.Value(int, 0)
center1 = manager.Value(int, 0)
center2 = manager.Value(int, 0)

image_arr = 0

##############################################################
# Functions
##############################################################

def Receiver(BUFFER_SIZE, number):
    while(1):
        try:
            #data = b''
            #data = net.Receive(BUFFER_SIZE)
            #print(data)
            #image_arr = np.frombuffer(data,np.uint8)
            w, h, c1, c2 = analysis.drone_detection(image_arr)
            Height.set(h)
            Width.set(w)
            center1.set(c1)
            center2.set(c2)

        except:
            print("died")

def tcpSender(yaw, pitch, number):
    tal = 0
    while(1):
        time.sleep(1)
        packet = net.packer(-154, 154)
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

def McCorrectionationingosåenmere():
    while(1):
        print("skal laves")
        imgList = [Height.get(), Width.get(), center1.get(), center2.get()]
        print(imgList[3])
        print(correction.motorCorrection(imgList, 53, 4,0,0)) #WHAT THE FUCK WHY DOESN'T THIS WOOOOOOOOOORKKKKKK!!!!!!!!!!!?!?!?!?!?!?!?!?
        

##############################################################
# Main
##############################################################

if __name__ == '__main__':
    try:
        #sendProcess = mp.Process(target=tcpSender, args=(yaw, pitch, number))
        receiveProcess = mp.Process(target=Receiver, args=(2048,number))
        #imgProcessor = mp.Process(target=imageProcessProcess,)
        McCProcess = mp.Process(target=McCorrectionationingosåenmere, )


        receiveProcess.start()
        #sendProcess.start()
        #imgProcessor.start()
        McCProcess.start()
        receiveProcess.join()
        #sendProcess.join()
        #imgProcessor.join()
        McCProcess.join()
    except KeyboardInterrupt:
        print("Shutting down....")
        #sendProcess.terminate()
        receiveProcess.terminate()
        print("Bye")
