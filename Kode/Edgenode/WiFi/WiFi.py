import socket

#_________________________________________________________________________________________#
#_________________________________________Setup___________________________________________#
#_________________________________________________________________________________________#

FORMAT = 'utf-8'

# Setup ip and ports
Edge_IP = ''
Sentry_IP = ''
VIDEO_PORT = 2025
Command_PORT = 2024

# Addresses
Edgenode_ADDR = (Edge_IP, VIDEO_PORT)
Sentry_ADDR = (Sentry_IP, Command_PORT)

# Setup the sockets
video_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Find local ip and Input ip and socket into video_udp
video_udp.bind(Edgenode_ADDR) # Bind socket to ip and port.

command_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#_________________________________________________________________________________________#
#_____________________________________functions___________________________________________#
#_________________________________________________________________________________________#

# Decode video
def Decoder():
    print("Decoding") # reci

# Receive videofeed
def Receive(BUFFER_SIZE):
    data, addr = video_udp.recvfrom(BUFFER_SIZE) # recieve feed from Sentry unit 

    return data

# Send Commands
def Send(commands):
    print("Sending Commands...")
    command_udp.sendto(commands, Sentry_ADDR)

    