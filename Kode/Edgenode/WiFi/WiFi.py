import socket
import struct
import numpy as np
import time

##############################################################
# Setup
##############################################################


FORMAT = 'utf-8'

# Setup ip and ports
Edge_IP = '172.26.24.28'
Sentry_IP = '172.26.24.184'

VIDEO_PORT = 2024
Command_PORT = 2025

# Addresses
Edgenode_ADDR = (Edge_IP, VIDEO_PORT)   # Edgenode address
Sentry_ADDR = (Sentry_IP, Command_PORT) # Sentry unit address

# Setup the sockets
video_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Find local ip and Input ip and socket into video_udp
video_udp.bind(Edgenode_ADDR) # Bind socket to ip and port.
#video_udp.settimeout(2) # set timeout for the receiving socket such that it gives an error if exceeded.
command_udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket for commands
command_udp.settimeout(2)

##############################################################
# Functions
##############################################################

def Receive(BUFFER_SIZE, oldnum): # Receive videofeed udp
    # timestart = time.time()
    """
    The receive functions receives a package which contains the
    sequence number, an image and the length of the image.
    It then unpacks the image into a numpy.array
    
    :param BUFFER_SIZE: Used to define how big the buffer should be.
    :returns: image, image length, sequence number
    """

    data, addr = video_udp.recvfrom(BUFFER_SIZE) # recieve feed from Sentry unit
    header = data[:20]
    sequenceNum, imgLen, datid, totalpackets, datalen = struct.unpack("<IIIII", header)

    imageLength = imgLen
    imagearr = [data[20:]]
    # print("Pakke: ",datid, " Ud af: ", totalpackets)
    oldSequenceNum = sequenceNum
    
    if totalpackets != 1:
        while True:
            data, addr = video_udp.recvfrom(BUFFER_SIZE) # recieve feed from Sentry unit
            header = data[:20]
            sequenceNum, imgLen, datid, totalpackets, datalen = struct.unpack("<IIIII", header)
            if sequenceNum <= oldSequenceNum:
                sequenceNum = 0
                raise("Received old packets")
            oldSequenceNum == sequenceNum
            print("Pakke: ",datid+1, " Ud af: ", totalpackets)
            imagearr.append(data[20:])
            if datid >= totalpackets-1:
                break

    # for i in range (totalpackets-1):
    #     data, addr = video_udp.recvfrom(BUFFER_SIZE) # recieve feed from Sentry unit
    #     imagearr.append(data[20:])
     
    fullimage = b''.join(imagearr)

    return fullimage, oldSequenceNum

def Send(commands): # UDP communication for commands
    command_udp.sendto(commands, Sentry_ADDR) 

def tcpSend(commands): # TCP communication for commands
    """
    The tcpSend function sends commands to the Sentry unit via TCP.
    It takes a struct object with bytes and send them.
    
    :param commands: Used to Send a struct object of command-bytes to the sentry unit.
    :returns: Nothing
    """
    try:
        command_udp.sendall(commands)
    except:
        command_udp.connect(Sentry_ADDR)
        command_udp.sendall(commands)
    #command_udp.close()

def closeDown():
    command_udp.close()

