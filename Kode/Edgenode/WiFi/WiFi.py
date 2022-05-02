import socket
import struct

#_________________________________________________________________________________________#
#_________________________________________Setup___________________________________________#
#_________________________________________________________________________________________#

FORMAT = 'utf-8'

# Setup ip and ports
Edge_IP = '127.0.0.1'
Sentry_IP = '127.0.0.1'
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

#_________________________________________________________________________________________#
#_____________________________________functions___________________________________________#
#_________________________________________________________________________________________#

# Decode video

def packer(yaw,pitch):
    fullPack = struct.pack('hh', yaw, pitch)

    return fullPack

def Decoder():
    print("Decoding") # Decode video feed


def Receive(BUFFER_SIZE): # Receive videofeed udp
    data, addr = video_udp.recvfrom(BUFFER_SIZE) # recieve feed from Sentry unit 

    return data


def Send(commands): # UDP communication for commands
    command_udp.sendto(commands, Sentry_ADDR) 


def tcpSend(commands): # TCP communication for commands
    command_udp.connect(Sentry_ADDR)
    command_udp.send(commands)
    command_udp.close()
