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
    return struct.pack("<BB", yawCmd , pitchCmd )


yaw = createCmd(-24, 3)
pitch = createCmd(12, 1)
res = packCmds(yaw, pitch)
print(hex(yaw), hex(pitch))

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('172.26.24.184', 2025))
yawAngles = [0, -15, 20, 14, -3]
yawSpeed  = [0,  1,  3,  2, 0]
pitchAngles = [0, 23, -12, 24, 6]
pitchSpeed  = [2,  1,  1,  2, 3]


for i in range(len(yawAngles)):
    print(f"""Sending command with values:
Yaw angle: {yawAngles[i]}
Yaw speed: {yawSpeed[i]}
Pitch angle: {pitchAngles[i]}
Pitch speed: {pitchSpeed[i]}
""")
    yaw = createCmd(yawAngles[i], yawSpeed[i])
    pitch = createCmd(pitchAngles[i], pitchSpeed[i])
    res = packCmds(yaw, pitch)
    s.sendall(res)
s.close()
