""" Kilder
https://stackoverflow.com/questions/58469297/how-do-i-calculate-the-yaw-pitch-and-roll-of-a-point-in-3d
https://mathinsight.org/spherical_coordinates
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import misc
from math import cos, atan2, degrees, sqrt, pow, pi
import numpy as np
from time import time

def _time(f):
    def wrapper(*args):
        start = time()
        r = f(*args)
        end = time()
        print("%s timed %f\n" % (f.__name__, end-start) )
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
        return r
    return wrapper

def Recalibrate(ipList):
	"""
	Calibrates drone coordinates to be relative to camera coordinates

	Input:
	(Camera coordinates and Drone coordinates)[list]

	output:
	(Camera coordinates and Drone coordinates)[list] appended with New Drone Coordinates[list]
	"""
	ipList.append(ipList[2]-ipList[0])
	ipList.append(ipList[3]-ipList[0])
	return ipList


def calculateVector(recCoord):
	"""

	"""
	vector = sqrt(pow(recCoord[0],2)+pow(recCoord[1],2))
	return vector

def SpeedSetting(ipList, numSettings):
	"""
	Calculates desired speed setting based on vector to the drone

	Input:
	Recalibrated Drone Coordinates[list], Center of image[list], Number of speed settings[int]

	Output:
	Speed setting[int]
	"""
	outEdge = (calculateVector([(ipList[0]*2),(ipList[1]*2)]))/2 			# Testing what the longest possible vector is
	rangeList = [0 for x in range(numSettings)] 							# creating a list containing speedsetting ranges
	
	for x in range(numSettings):											# Filling the speedsetting ranges with largestVector/numberOfSettings*iteration
		rangeList[x] = outEdge/numSettings*(x+1)							
	
	vector = calculateVector([ipList[4],ipList[5]])							# Calculating the vector from camera center to the drone center
	
	for x in range(numSettings):											# Checking to see which speed seetting the vector corresponds to
		if (vector<=rangeList[x]):										
			speed = x
			break
	
	return speed

def getPitchYaw(ipList):
	"""
	Calculates pitch and yaw that the Sentry Unit should move

	Input:
	Image Processing output [list] appended with recalibrated drone coordinates

	Output:
	pitch(degree)[int], yaw(degree)[int]
	"""
	if ((ipList[4] == 0) and (ipList[5] == 0)):								# Checking to see if the camera center and the drone center is the same
		yOutput = 0
		pOutput = 0
	
	elif (ipList[4] == 0):													# Checkting to see if the yaw is correct but the pitch is not
		yOutput = 0
		pOutput = 90*(ipList[5]/ipList[1])
	
	elif (ipList[5] == 0):													# Checking to see if the pitch is correct but the yaw is not
		yOutput = 90*(ipList[4]/ipList[0])
		pOutput = 0
	
	else:
		yOutput = atan2(ipList[5], ipList[4])								# Checking to see in which half the drone is located, y > 0 or y < 0
		
		if (yOutput < 0):													# if y < 0							
			if yOutput < -(pi/2):												# checking if x < 0
				yOutput = atan2(ipList[4], ipList[5])						
				yOutput += pi
				yOutput = -yOutput	
			else:																# if x >= 0
				yOutput = atan2(ipList[4], ipList[5])
				yOutput -= (pi)
				yOutput = abs(yOutput) 
			pOutput = -((pi/2)-abs(yOutput))									# subtracting the yaw from 90 degrees to get the pitch

		else:																# if y >= 0 
			if yOutput > (pi/2):												# checking if x < 0
				yOutput = atan2(ipList[4], ipList[5])						
			else:																# if x >= 0
				yOutput = atan2(ipList[4], ipList[5])
			pOutput = (pi/2)-abs(yOutput)										# subtracting the yaw from 90 degrees to get the pitch

		yOutput = round(degrees(yOutput), 0)								# Converting yOutput and pOutput from rad to degrees 
		pOutput = round(degrees(pOutput), 0)
	
	return pOutput, yOutput 

@_time
def motorControl(ipList, numberOfSettings, printOut=0):
	"""
	Takes image process output and producces pitch, yaw and speed setting

	input:
	Image Center is the first x =[0] y = [1] and Drone center is x = [2] y = [3]

	Output:
	pitch(degree)[int], yaw(degree)[int], speed[int]
	"""
	Recalibrate(ipList)
	speed = SpeedSetting(ipList, numberOfSettings)
	pitch, yaw = getPitchYaw(ipList)

	if (printOut != 0):
		print("\nInput:\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
		print(f'Camera center coordinates are:\t\t[{ipList[0]},{ipList[1]}]\n\n')
		print(f'Drone center coordinates are:\t\t[{ipList[2]},{ipList[3]}]\n\n')
		print(f'Drone relative to the camera center:\t[{ipList[4]},{ipList[5]}]\n')
		print("Output:\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
		print(f'The Speed setting: {speed} out of {numberOfSettings-1}\n\n')
		print(f'Yaw in degrees: {yaw} \n\n')
		print(f'Pitch in degrees: {pitch} \n')
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
	return	 pitch, yaw, speed


if __name__=="__main__":   
	ImProcOutput = [5,5,3,2]
	NumberOfSpeedSettings = 4
	motorControl(ImProcOutput,NumberOfSpeedSettings,1)