import struct
import math

yawAngle = 4
yawSpeed = 1
pitchAngle = 2
pitchSpeed = 6

def packer(yawAngle,pitchAngle,yawSpeed,pitchSpeed):
    fullPack = struct.pack('hBhB', yawAngle, yawSpeed, pitchAngle,pitchSpeed)

    return fullPack

print(packer(yawAngle,pitchAngle,yawSpeed,pitchSpeed))


