import struct
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(("0.0.0.0", 2024))

def unpackHeader(data):
    header = data[:20]
    sequence, imgLen, datid, totalpackets, datalen = struct.unpack("<IIIII", header)

    print("[SEQ]: ",sequence,
          "[IMGLEND]: ", imgLen,
          "[DATID]: ", datid,
          "[TOTALPACKETS]: ", totalpackets,
          "[DATALEN]: ", datalen)
    
while True:
    try:
        data, addr = sock.recvfrom(65000)
    except socket.error as e:
        print(e)
    else:
        unpackHeader(data)
