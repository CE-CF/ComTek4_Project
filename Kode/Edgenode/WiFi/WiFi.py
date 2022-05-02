import socket
import struct

##############################################################
# Setup
##############################################################


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


##############################################################
# Functions
##############################################################

def packer(yaw,pitch):
    """
    The packer function packs the yaw and pitch values into a byte string.
    The yaw and pitch values are passed to the function as arguments,
    and they are stored in an array of bytes called fullPack. The two numbers
    are then packed together using struct.pack() which takes two arguments:
    
        1) 'hh' - This specifies that we're packing two signed short integers (int).
    
        2) The second argument is where the data is actually packed into our bytestring, fullPack. 
           It's done one after another because struct only packs items in tuples/sequences 
           (i.e., arrays). Since we have two items here, they get put in there one after another.
    
    :param yaw: Used to Control the direction that the drone is facing.
    :param pitch: Used to Control the pitch of the drone.
    :return: A byte object that is the concatenation of the two values passed to it.
    
    :doc-author: Trelent
    """
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
    """
    The tcpSend function sends commands to the Sentry via TCP.
    It takes a list of commands as an argument, and sends them one by one.
    
    :param commands: Used to Send a list of commands to the sentry.
    :return: The number of bytes sent.
    
    :doc-author: Trelent
    """
    command_udp.connect(Sentry_ADDR)
    command_udp.send(commands)
    command_udp.close()
