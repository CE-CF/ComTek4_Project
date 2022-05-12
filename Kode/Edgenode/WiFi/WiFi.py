import socket
import struct
import numpy as np

##############################################################
# Setup
##############################################################


FORMAT = 'utf-8'

# Setup ip and ports
Edge_IP = '192.168.1.123'
Sentry_IP = '192.168.1.238'

VIDEO_PORT = 2025
Command_PORT = 2024

# Addresses
Edgenode_ADDR = (Edge_IP, VIDEO_PORT)   # Edgenode address
Sentry_ADDR = (Sentry_IP, Command_PORT) # Sentry unit address

# Setup the sockets
video_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Find local ip and Input ip and socket into video_udp
video_udp.bind(Edgenode_ADDR) # Bind socket to ip and port.
video_udp.settimeout(2) # set timeout for the receiving socket such that it gives an error if exceeded.
command_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create socket for commands


##############################################################
# Variables
##############################################################

sequenceRef = 0

##############################################################
# Functions
##############################################################

def Receive(BUFFER_SIZE): # Receive videofeed udp
    """
    The receive functions receives a package which contains the
    sequence number, an image and the length of the image.
    It then unpacks the image into a numpy.array
    
    :param BUFFER_SIZE: Used to define how big the buffer should be.
    :returns: image, image length, sequence number
    """
    data, addr = video_udp.recvfrom(BUFFER_SIZE) # recieve feed from Sentry uni
    
    sequenceNum = data[:2]
    imgLength = int.from_bytes(data[2:4], big)
    image = data[4:]

    if sequenceNum < sequenceRef:
        raise ValueError("Old image")
    if len(image) != int.from_bytes(imgLength, big):
        raise ValueError("package damaged")
    sequenceRef = sequenceNum
    image = np.fromstring(image,np.uint8)
    return image

def Send(commands): # UDP communication for commands
    command_udp.sendto(commands, Sentry_ADDR) 

def tcpSend(commands): # TCP communication for commands
    """
    The tcpSend function sends commands to the Sentry unit via TCP.
    It takes a struct object with bytes and send them.
    
    :param commands: Used to Send a struct object of command-bytes to the sentry unit.
    :returns: Nothing
    """
    command_udp.connect(Sentry_ADDR)
    command_udp.send(commands)
    command_udp.close()
