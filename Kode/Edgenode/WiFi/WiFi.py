import socket

BUFFER_SIZE = 2048
FORMAT = 'utf-8'

# Setup ip and ports
Edge_IP = ''
Sentry_IP = ''
VIDEO_PORT = 2025

# Addresses
Edgenode_ADDR = (Edge_IP, VIDEO_PORT)
Sentry_ADDR = (Sentry_IP, VIDEO_PORT)

# Setup the socket
video_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Find local ip and Input ip and socket into video_udp
video_udp.bind(Edgenode_ADDR) # Bind socket to ip and port.

# Receive videofeed
def Rvideofeed():
    data, addr = video_udp.recvfrom(BUFFER_SIZE) # recieve feed from Sentry unit
    
    # DECODE VIDEO HERE

    # SEND VIDEO TO GUI and IMGPROCESS processes.

