import socket
import struct

##############################################################
# Setup
##############################################################


FORMAT = 'utf-8'

# Setup ip and ports
Edge_IP = '192.168.1.197'
Sentry_IP = '192.168.1.238'

commands = drone.jpg

VIDEO_PORT = 2025
Command_PORT = 2024

# Addresses
Edgenode_ADDR = (Edge_IP, VIDEO_PORT)   # Edgenode address
Sentry_ADDR = (Sentry_IP, Command_PORT) # Sentry unit address

command_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create socket for commands


##############################################################
# Functions
##############################################################

def Send(commands): # UDP communication for commands
    command_udp.sendto(commands, Sentry_ADDR) 
