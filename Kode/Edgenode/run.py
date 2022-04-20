import WiFi.WiFi
import multiprocessing
import socket
import time

net = WiFi.WiFi

data = b''
msg = b'0,0,0'

def Receiver(BUFFER_SIZE):
    while(1):
        try:
            data = net.Receive(BUFFER_SIZE)
        except:
            print("Didn't receive anything")
      

def Sender(commands):
    while(1):
        print("sending commands")
        net.Send(commands)

if __name__ == '__main__':
    sendProcess = multiprocessing.Process(target=Sender, args=(msg,))
    receiveProcess = multiprocessing.Process(target=Receiver, args=(2048,))

    receiveProcess.start()
    sendProcess.start()
