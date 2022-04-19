import WiFi.WiFi
import multiprocessing

net = WiFi.WiFi

data = b''
commands = (0,0,0)

def Receiver(BUFFER_SIZE):
    data = net.Receive(BUFFER_SIZE)

def Sender(commands):
    net.Send(commands)

if __name__ == '__main__':
    receiveProcess = multiprocessing.process(target=Receiver(2048))
    sendProcess = multiprocessing.process(target=Sender(),args=(commands))