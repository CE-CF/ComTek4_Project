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


def Recalibrate(ipList):
	"""
	Calibrates drone coordinates to be relative to camera coordinates

	Input:
	(Camera coordinates and Drone coordinates)[list]

	output:
	New Drone Coordinates[list]
	"""
	newDroneCoord = [0,0]
	newDroneCoord[0] = ipList[2]-ipList[0]
	newDroneCoord[1] = ipList[3]-ipList[1]
	return newDroneCoord


def Magnitude(recCoord):
	magnitude = sqrt(pow(recCoord[0],2)+pow(recCoord[1],2))
	return magnitude

def SpeedSetting(recCoord, ipList, numSettings):
	"""
	Calculates desired speed setting based on vector to the drone

	Input:
	Recalibrated Drone Coordinates[list], Center of image[list], Number of speed settings[int]

	Output:
	Speed setting[int]
	"""
	outEdge = Magnitude([(ipList[0]*2),(ipList[1]*2)])
	rangeList = [0, outEdge/numSettings, (outEdge/numSettings)*2, (outEdge/numSettings)*3, outEdge]
	magnitude = Magnitude(recCoord)

	if (magnitude<rangeList[1]):
		speed = 0
	elif (magnitude<rangeList[2]):
		speed = 1
	elif (magnitude<rangeList[3]):
		speed = 2
	elif (magnitude<rangeList[4]):
		speed = 3
	return speed

def getPitchYaw(recCoord):
	"""
	Calculates pitch and yaw that the Sentry Unit should move

	Input:
	Recalibrated drone coordinates

	Output:
	pitch(degree)[int], yaw(degree)[int]
	"""
	pOutput = atan2(recCoord[0],recCoord[1])
	yOutput = (pi/2)-pOutput
	pOutput = round(degrees(pOutput), 0)
	yOutput = round(degrees(yOutput),0)
	return pOutput, yOutput 

def motorControl(ipList, printOut=0):
	"""
	Takes image process output and producces pitch, yaw and speed setting

	input:
	Image Center is the first x =[0] y = [1] and Drone center is x = [2] y = [3]

	Output:
	pitch(degree)[int], yaw(degree)[int], speed[int]
	"""
	recDroneCoord = Recalibrate(ipList)
	numberOfSettings = 4
	speed = SpeedSetting(recDroneCoord, ipList, numberOfSettings)
	pitch, yaw = getPitchYaw(recDroneCoord)

	if (printOut != 0):
		print(f'Mid of image coordinates are: [{ipList[0]},{ipList[1]}]\n\n')
		print(f'The drone in located at: [{ipList[2]},{ipList[3]}]\n\n')
		print(f'The Speed setting: {speed}\n\n')
		print(f'Yaw in degrees: {yaw} \n\n')
		print(f'Pitch in degrees: {pitch} \n\n')
	return pitch, yaw, speed


imageoutput = [3,3,4,5]
motorControl(imageoutput, 1)