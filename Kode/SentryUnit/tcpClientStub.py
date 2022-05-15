import socket
import struct


def createCmd(angle, speed):
    signMSK = 0b10000000
    speedMSK = 0b01100000
    angleMSK = 0b00011111
    result = 0b00000000

    if angle < 0:
        result += (abs(angle) & angleMSK) | signMSK
    else:
        result += (abs(angle) & angleMSK)

    result += (speed << 5) & speedMSK

    return result


def packCmds(yawCmd, pitchCmd):
    return struct.pack("<hh", yawCmd, pitchCmd)


yaw = createCmd(31, 3)
pitch = createCmd(25, 2)

res = packCmds(yaw, pitch)
print(res, len(res))
print(bin(res[0]), bin(res[2]))

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('192.168.1.48', 2025))

s.sendall(res)
s.close()
