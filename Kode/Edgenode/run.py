import WiFi.WiFi
import ImgProcess.Img_process as analysis
import McC.McC as correction
import GUI.gui as dinmor
import multiprocessing as mp
import socket, time, struct, math
import numpy as np
import cv2
import pickle


##############################################################
# Renaming
##############################################################

net = WiFi.WiFi
manager = mp.Manager()

##############################################################
# Variables
##############################################################

bufferSize = 65000

##############################################################
# Variables: Shared memory
##############################################################

sharedFeed = manager.Value(bytes, 0xff)
detected = manager.Value(int, 0)
created = manager.Value(int, 0)

center1 = manager.Value(int, 0)
center2 = manager.Value(int, 0)
drone1 = manager.Value(int, 0)
drone2 = manager.Value(int, 0)

yawC = manager.Value(int, 0)
pitchC = manager.Value(int, 0)

##############################################################
# Variables: Timer
##############################################################
starttime = manager.Value(int, 0)
endtime = manager.Value(int, 0)

receivetimeStart = manager.Value(int, 0)
receivetimeEnd = manager.Value(int, 0)

SendtimeStart = manager.Value(int, 0)
SendtimeEnd = manager.Value(int, 0)

imgtimeStart = manager.Value(int, 0)
imgtimeEnd = manager.Value(int, 0)


McCtimeStart = manager.Value(int, 0)
McCtimeEnd = manager.Value(int, 0)


stoptime = manager.Value(int, 0)

##############################################################
# Functions
##############################################################


def Receiverimg(BUFFER_SIZE):
    timedR = 0
    starttime.set(time.time())
    DAmount = 0
    imgtimer = 0
    imagereceived = 0
    oldSequenceNum = 0
    while(1):
        try:
            receivetime1 = (time.time())
            image, oldSequenceNum = net.Receive(BUFFER_SIZE, oldSequenceNum)
            sharedFeed.set(image)
            c1, c2, d1, d2 = analysis.drone_detection(sharedFeed.get())
            if d1 and d2 == 0:
                drone1.set(d1)
                drone2.set(d2)
                DAmount = 0
                detected.set(0)
            else:
                DAmount = DAmount + 1
            if DAmount > 4:
                #print(c1,c2,d1, d2)
                center1.set(c2)
                center2.set(c1)
                drone1.set(d1)
                drone2.set(d2)
                detected.set(1)
                # if imgtimer == 0:
                #     imgtimeEnd.set(time.time())
            if imagereceived < 5:
                receivetime2 = (time.time())
                print(receivetime2 - receivetime1, "Stop: ", receivetime2, "Start: ",receivetime1)
                imagereceived += 1
            if imagereceived > 4:
                stoptime.set(1)
        except:
            print("Failed to receive...")

##############################
# Receive function
##############################

def Receiver(BUFFER_SIZE):
    timedR = 0
    starttime.set(time.time())
    receivetimeStart.set(time.time())
    while(1):
        try:
            image = net.Receive(BUFFER_SIZE)
            sharedFeed.set(image)
            if timedR == 0:
                timedR = 1
        except:
            print("Failed to receive...")
        


##############################
# Send function
##############################

def tcpSender():
    connect = 0
    timerdone = 0
    SendtimeStart.set(time.time())
    while(1):
        try:
            net.command_udp.connect(net.Sentry_ADDR)
        except:
            pass    
        try:
            # print("Detected: ", detected.get())
            if detected.get() == 1 and yawC.get() != 0 and pitchC != 0:
                # print("Yaw: ",yawC.get(), " Pitch: ", pitchC.get())
                packet = struct.pack('bb', yawC.get(), pitchC.get())
                print(packet)
                # print("sending commands..")
                net.tcpSend(packet,connect)
                #print("commands sent")
                connect = 1
                if stoptime.get() == 1:
                    if timerdone == 0:
                        SendtimeEnd.set(time.time())
                        endtime.set(time.time())
                        print(endtime.get()-starttime.get(),"Endtime: " ,endtime.get(), "Starttime" , starttime.get())
                        timerdone = 1
        except:
            # print("Failed to send...")
            pass

##############################
# Image Processing function
##############################

def imageProcessProcess():
    DAmount = 0
    imgtimer = 0
    # time.sleep(0.5)
    # imgtimeStart.set(time.time())
    while(1):
        # print("here")
        c1, c2, d1, d2 = analysis.drone_detection(sharedFeed.get())
        if d1 and d2 == 0:
            drone1.set(d1)
            drone2.set(d2)
            DAmount = 0
            detected.set(0)
        else:
            DAmount = DAmount + 1
        if DAmount > 4:
            #print(c1,c2,d1, d2)
            center1.set(c2)
            center2.set(c1)
            drone1.set(d1)
            drone2.set(d2)
            detected.set(1)
            # if imgtimer == 0:
            #     imgtimeEnd.set(time.time())

##############################
# Motor Correction function
##############################

def McCorrection():
    correctionList = 1
    timerMcC = 0
    with open("/home/madss/Documents/school/4S/projekt/ComTek4_Project/correctionList.pkl", 'rb') as f:
        correctionList = pickle.load(f)
    while(1):
        # print(f'detected: {detected.get()}')
        if drone1.get() != 0 and drone2.get() != 0:
            if detected.get() == 1:
                # print(f'created: {created.get()}')
                if created.get() != 1:
                    created.set(1)
                    imgList = [center1.get(), center2.get(), drone1.get(), drone2.get()]
                    yaw, pitch = correction.motorCorrection(imgList, 53, 4,correctionList,1,0)
                    yawC.set(yaw)
                    pitchC.set(pitch)
                    with open("/home/madss/Documents/school/4S/projekt/ComTek4_Project/correctionList.pkl", 'rb') as f:
                        correctionList = pickle.load(f)
                else: 
                    imgList = [center1.get(), center2.get(), drone1.get(), drone2.get()]
                    # print(imgList)
                    yaw, pitch = correction.motorCorrection(imgList, 53, 4,correctionList,1,timerMcC)
                    timerMcC = 0
                    yawC.set(yaw)
                    pitchC.set(pitch)
  
##############################
# Gui function 
##############################

def Guiprocessfunction():
    time.sleep(2)
    while(1):
        try:
            dinmor.gui(sharedFeed.get(), yawC.get(), pitchC.get())
        except:
            pass

##############################################################
# Main
##############################################################

if __name__ == '__main__':
    try:
        sendProcess = mp.Process(target=tcpSender,)
        # receiveProcess = mp.Process(target=Receiver, args=(bufferSize,))
        # imgProcessor = mp.Process(target=imageProcessProcess,)
        receiveimgProcess =mp.Process(target=Receiverimg, args=(bufferSize,))
        McCProcess = mp.Process(target=McCorrection,)
        Guiprocess = mp.Process(target=Guiprocessfunction,)

        # receiveProcess.start()
        sendProcess.start()
        # imgProcessor.start()
        McCProcess.start()
        Guiprocess.start()
        receiveimgProcess.start()
        # receiveProcess.join()
        sendProcess.join()
        # imgProcessor.join()
        McCProcess.join()
        receiveimgProcess.join()
        Guiprocess.join()
    except KeyboardInterrupt:
        print("Shutting down....")
        net.closeDown()
        sendProcess.terminate()
        # receiveProcess.terminate()
        # imgProcessor.terminate()
        McCProcess.terminate()
        Guiprocess.terminate()
        receiveimgProcess.terminate()
        print("Bye")
