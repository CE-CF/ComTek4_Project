import struct
import math

yawAngle = 4
yawSpeed = 1
pitchAngle = 2
pitchSpeed = 6

def packer(yawAngle,pitchAngle,yawSpeed,pitchSpeed):
    fullPack = struct.pack('hh', 122, 4) # yaw 26 grader speed setting 3 og Pitch: 4 grader, speed setting 0

    return fullPack

print(packer(yawAngle,pitchAngle,yawSpeed,pitchSpeed))



print('\xc7')
