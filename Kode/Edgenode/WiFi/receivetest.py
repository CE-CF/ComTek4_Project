import socket
import time

##############################################################
# Setup
##############################################################

FORMAT = 'utf-8'

Modtager_IP = '127.0.0.1'
Command_PORT = 2024
BUFFER_SIZE = 4048

# Addresses
Modtager_ADDR = (Modtager_IP, Command_PORT) # Sentry unit address

# Setup the sockets
modtager_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Find local ip and Input ip and socket into video_udp
modtager_udp.bind(Modtager_ADDR) # Bind socket to ip and port.


##############################################################
# Functions
##############################################################


def Receive(BUFFER_SIZE): # Receive videofeed udp
    data, addr = video_udp.recvfrom(BUFFER_SIZE) # recieve feed from Sentry unit 

    print(data)

while(1):
    Receive(BUFFER_SIZE)