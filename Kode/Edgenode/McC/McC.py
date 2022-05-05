"""Kilder
https://stackoverflow.com/questions/58469297/how-do-i-calculate-the-yaw-pitch-and-roll-of-a-point-in-3d
https://mathinsight.org/spherical_coordinates
"""
import os
from math import atan2, degrees, pi
import numpy as np
from time import time
import pickle

def _time(f):
    def wrapper(*args):
        start = time()
        r = f(*args)
        end = time()
        print("%s timed %f" % (f.__name__, end-start) )			# \033[F print up one line to not interefere with normal print without timer
        return r
    return wrapper

def cameraOrientation(ipList, cameraFOV):
	if (ipList[0] > ipList[1]): 
		cameraFOVx = cameraFOV
		cameraFOVy = ipList[1]/ipList[0]*cameraFOV
	
	elif (ipList[0] < ipList[1]):
		cameraFOVy = cameraFOV
		cameraFOVx = ipList[1]/ipList[0]*cameraFOV
	
	else:
		cameraFOVy = cameraFOV
		cameraFOVx = cameraFOV
	return cameraFOVx, cameraFOVy

def Recalibrate(ipList):
	"""
	Calibrates drone coordinates to be relative to camera coordinates
	
	Args:
	    ipList (list): Camera coordinates and Drone coordinates
	
	Returns:
	    ipList (list): Camera coordinates and Drone coordinates appended with New Drone Coordinates
	"""
	ipList.append(ipList[2]-ipList[0])
	ipList.append(ipList[3]-ipList[1])
	return ipList

def SpeedSetting(ipList, numSettings):
	"""
	Calculates desired speed setting based on vector to the drone
	
	Args:
	    ipList (list): 		Camera coordinates and Drone coordinates appended with New Drone Coordinates
	    numSettings (int): 	Number of speed settings
	
	Returns:
	    pSpeed (int): 		The correction speed for pitch motor
	    ySpeed (int): 		The correction speed for yaw motor
	"""
	pOutEdge = ipList[1]												# Testing what the longest possible vector is
	pRangeList = [0 for x in range(numSettings)] 	

	yOutEdge = ipList[0] 												# Testing what the longest possible vector is
	yRangeList = [0 for x in range(numSettings)] 						# creating a list containing speedsetting ranges
	
	for x in range(numSettings):											# Filling the speedsetting ranges with largestVector/numberOfSettings*iteration
		pRangeList[x] = pOutEdge/numSettings*(x+1)							
		yRangeList[x] = yOutEdge/numSettings*(x+1)
	
	yVector = abs(ipList[4])											# Calculating the vector from camera center to the drone center
	pVector = abs(ipList[5])

	for x in range(numSettings):
		if (pVector<=pRangeList[x]):										
			pSpeed = x
			break
	for x in range(numSettings):										# Checking to see which speed seetting the vector corresponds to
		if (yVector<=yRangeList[x]):
			ySpeed = x
			break

	return pSpeed, ySpeed

def getPitchYaw(ipList, xfov, yfov):
	"""
	Calculates pitch and yaw that the Sentry Unit should move
	
	Args:
	    ipList (TYPE): 	Camera coordinates and Drone coordinates appended with New Drone Coordinates
		xfov (float):	Camera field of view on the x-axis
		yfov (float):	Camera field of view on the y-axis
	Returns:
	    yaw (int):		Sentry Unit yaw movement in degrees
	    pitch (int):	Sentry Unit pitch movement in degrees
	"""
	if ((ipList[4] == 0) and (ipList[5] == 0)):								# Checking to see if the camera center and the drone center is the same
		yaw = 0
		pitch = 0
	
	elif (ipList[4] == 0):													# Checkting to see if the yaw is correct but the pitch is not
		yaw = 0
		pitch = yfov/2*(ipList[5]/ipList[1])
		
	elif (ipList[5] == 0):													# Checking to see if the pitch is correct but the yaw is not
		yaw = xfov/2*(ipList[4]/ipList[0])
		pitch = 0
	else:
		if (ipList[4]<0):
			yaw = xfov/2*(ipList[4]/ipList[0])
			print(f'yaw = -xfov/2*(ipList[4]/ipList[0]) = {yaw}')
		else:
			yaw = xfov/2*(ipList[4]/ipList[0])
			print(f'yaw = xfov/2*(ipList[4]/ipList[0]) = {yaw}')
		if (ipList[5]<0):
			pitch = yfov/2*(ipList[5]/ipList[1])
			print(f'pitch = -yfov/2*(ipList[5]/ipList[1]) = {pitch}')
		else:
			pitch = yfov/2*(ipList[5]/ipList[1])
			print(f'pitch = yfov/2*(ipList[5]/ipList[1]) = {pitch}')
	return pitch, yaw 

@_time
def motorCorrection(ipList,cameraFOV, numberOfSettings, correctionList=0, printOut=0):
	"""
	Takes image process output and producces motor commands
	
	Args:
	    ipList (list): Camera Center ([0],[1]) and Drone center is ([2],[3])
	    cameraFOV (int): The Field of View for the camera
	    numberOfSettings (int): Number of speed settings
	    correctionList (int, list): if there is no correctionList input, the function will make one before returning result
		printOut (int, optional): set to 1 for print, remove
	
	Returns:
	    yaw (int):		Sentry Unit yaw movement in degrees
	    ySpeed (int): 	The correction speed for yaw motor
	    pitch (int):	Sentry Unit pitch movement in degrees
	    pSpeed (int)	The correction speed for yaw motor
	"""
	if (correctionList == 0):
		pickleList = [[[0 for x in range(4)]for y in range(ipList[1]*2)] for z in range(ipList[0]*2)]
		for x in range(ipList[0]*2):
			if (printOut != 0):
					if (x%100 == 0):
						print('We are currently at: {:4d} of {}'.format(x,ipList[0]*2))
			for y in range(ipList[1]*2):
				tmpList = [ipList[0],ipList[1],x,y]
				cameraFOVx, cameraFOVy = cameraOrientation(ipList, cameraFOV)
				Recalibrate(tmpList)
				pSpeed, ySpeed = SpeedSetting(tmpList, numberOfSettings)
				pitch, yaw = getPitchYaw(tmpList, cameraFOVx, cameraFOVy)
				pickleList[x][y] = [yaw,ySpeed,pitch,pSpeed]
		with open('correctionList.pkl', 'wb') as f:
			pickle.dump(pickleList, f)
		with open('correctionList.pkl', 'rb') as f:
			correctionList = pickle.load(f)

	yaw = correctionList[ipList[2]][ipList[3]][0]
	ySpeed = correctionList[ipList[2]][ipList[3]][1]
	pitch = correctionList[ipList[2]][ipList[3]][2]
	pSpeed = correctionList[ipList[2]][ipList[3]][3]

	if (printOut != 0):
		print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		print("                       Input\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
		print(f'Camera center coordinates are:\t\t[{ipList[0]},{ipList[1]}]\n\n')
		print(f'Drone center coordinates are:\t\t[{ipList[2]},{ipList[3]}]\n\n')
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		print("                       Output\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
		print('The pitch Speed setting in range 0 to {}:\t{:3d} \n\n'.format(numberOfSettings-1,pSpeed))
		print('Pitch in degrees:\t\t\t\t{:3d} \n\n'.format(int(pitch)))
		print('The yaw Speed setting in range 0 to {}:\t\t{:3d} \n\n'.format(numberOfSettings-1,ySpeed))
		print('Yaw in degrees:\t\t\t\t\t{:3d} \n'.format(int(yaw)))
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
	return	 yaw, ySpeed, pitch, pSpeed 


if __name__=="__main__":   

	NumberOfSpeedSettings = 4
	ImProcOutput = [960,540,0,0]
	cameraFOV = 53

	#motorCorrection(ImProcOutput,cameraFOV,NumberOfSpeedSettings,0,1)
	with open('correctionList.pkl', 'rb') as f:
		correctionList = pickle.load(f)
	motorCorrection(ImProcOutput,cameraFOV,NumberOfSpeedSettings,correctionList)