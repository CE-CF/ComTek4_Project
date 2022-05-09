"""Kilder
https://stackoverflow.com/questions/58469297/how-do-i-calculate-the-yaw-pitch-and-roll-of-a-point-in-3d
https://mathinsight.org/spherical_coordinates
"""
import os
from math import atan2, degrees, pi, floor
import numpy as np
import pickle
import time, sys
import argparse

# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 23 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rCreating correctionList: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), int(progress*100), status)
    sys.stdout.write(text)
    sys.stdout.flush()

def _time(f):
    def wrapper(*args):
        start = time.time()
        r = f(*args)
        end = time.time()
        if (args[5]!=0):
	        if (args[3] == 0):
	        	print("%s with list creation:   %f seconds" % (f.__name__, end-start))
	        else:
	        	if (args[4] == 0):
		        	print("%s with focus on time:    %f second" % (f.__name__, end-start))
		        else:
		        	print("%s with focus on space:   %f second" % (f.__name__, end-start))
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
			pSpeed = int(round(x,0))
			break
	for x in range(numSettings):										# Checking to see which speed seetting the vector corresponds to
		if (yVector<=yRangeList[x]):
			ySpeed = int(round(x,0))
			break

	return pSpeed, ySpeed

def getPitchYaw(ipList, xfov, yfov):
	"""
	Calculates pitch and yaw that the Sentry Unit should move
	
	Args:
	    ipList (list): 	Camera coordinates and Drone coordinates appended with New Drone Coordinates
		xfov (float):	Camera field of view on the x-axis
		yfov (float):	Camera field of view on the y-axis
	Returns:
	    yaw (int):		Sentry Unit yaw movement in degrees
	    pitch (int):	Sentry Unit pitch movement in degrees
	"""
	if ((ipList[4] == 0) and (ipList[5] == 0)):								# Checking to see if the camera center and the drone center is the same
		yaw = 0
		pitch = 0
	elif (ipList[4] == 0):
		yaw = 0
		pitch = int(round(yfov/2*(ipList[5]/ipList[1]),0))
	elif (ipList[5] == 0):
		pitch = 0
		yaw = int(round(xfov/2*(ipList[4]/ipList[0]),0))
	else:
		yaw = int(round(xfov/2*(ipList[4]/ipList[0]),0))
		pitch = int(round(yfov/2*(ipList[5]/ipList[1]),0))
	return pitch, yaw 

def packData(yDegree, ySpeed, pDegree, pSpeed, numSettings):
	"""
	Takes degrees and speedsetting for the Sentry Unit and packs it.	
	Args:
	    yDegree (int): 		Sentry Unit yaw movement in degrees
	    ySpeed (int): 		The correction speed for yaw motor
	    pDegree (int):		Sentry Unit pitch movement in degrees
	    pSpeed (int):		The correction speed for yaw motor
	    numSettings (int):	The number of speed settings
	
	Returns:
	   yawPacked (int):		A bit representation of yaw degree and speed
	   pitchPacked (int):	A bit representation of pitch degree and speed
	"""
	speedSetting = [pow(2,5)*x for x in range(numSettings)]
	#print(speedSetting)
	if (yDegree < 0):
		yawPacked = -(abs(yDegree)+speedSetting[ySpeed])
	else:
		yawPacked = yDegree+speedSetting[ySpeed]
	if (pDegree < 0):
		pitchPacked = -(abs(pDegree)+speedSetting[pSpeed])
	else:
		pitchPacked = pDegree+speedSetting[pSpeed]
	return yawPacked, pitchPacked

@_time
def motorCorrection(ipList,cameraFOV, numberOfSettings, correctionList=0, timeOrSpace=0, printOut=0):
	"""
	Takes image process output and producces motor commands
	
	Args:
	    ipList (list): Camera Center ([0],[1]) and Drone center is ([2],[3])
	    cameraFOV (int): The Field of View for the camera
	    numberOfSettings (int): Number of speed settings
	    correctionList (int, list): if there is no correctionList input, the function will make one before returning result
	    timeOrSpace (int, optional): If set to 0 the focus is on time, if set to 1 it is on space
		printOut (int, optional): set to 1 for print, remove
	
	Returns:
	   yawPacked (int):		A bit representation of yaw degree and speed
	   pitchPacked (int):	A bit representation of pitch degree and speed
	"""
	if (correctionList == 0):
		if (timeOrSpace == 0):
			pickleList = [[[0 for x in range(2)]for y in range(ipList[1]*2)] for z in range(ipList[0]*2)]
		else:
			pickleList = [[[0 for x in range(2)]for y in range(ipList[1]*2)] for z in range(ipList[0]*2)]

		for x in range(ipList[0]):
			if (printOut != 0):
				update_progress((x/(ipList[0])))
			for y in range(ipList[1]):
				tmpList = [ipList[0],ipList[1],x,y]
				cameraFOVx, cameraFOVy = cameraOrientation(ipList, cameraFOV)
				Recalibrate(tmpList)
				pSpeed, ySpeed = SpeedSetting(tmpList, numberOfSettings)
				pitch, yaw = getPitchYaw(tmpList, cameraFOVx, cameraFOVy)
				yawPacked, pitchPacked = packData(yaw, ySpeed,pitch,pSpeed,numberOfSettings)
				
				if (timeOrSpace == 0):
					pickleList[x][y] = [yawPacked, pitchPacked]
					pickleList[ipList[0]*2-(x+1)][y] = [-1*yawPacked, pitchPacked]
					pickleList[x][ipList[1]*2-(y+1)] = [yawPacked, -1*pitchPacked]
					pickleList[ipList[0]*2-(x+1)][ipList[1]*2-(y+1)] = [-1*yawPacked, -1*pitchPacked]
				else:
					pickleList[x][y] = [yawPacked, pitchPacked]
				

		with open('correctionList.pkl', 'wb') as f:
			pickle.dump(pickleList, f)
		with open('correctionList.pkl', 'rb') as f:
			correctionList = pickle.load(f)

	if (timeOrSpace == 0):
		yawPacked, pitchPacked = correctionList[ipList[2]][ipList[3]]
	else:
		if (ipList[2] <= ipList[0] and ipList[3] <=ipList[1]):
			yawPacked, pitchPacked = correctionList[ipList[2]][ipList[3]]
		
		if (ipList[3] <=ipList[1]):
			yawPacked, pitchPacked = correctionList[(ipList[0]*2)-ipList[2]][ipList[3]]
			yawPacked = -1*yawPacked

		if (ipList[2] <= ipList[0]):
			yawPacked, pitchPacked = correctionList[ipList[2]][(ipList[1]*2)-ipList[3]]
			pitchPacked = -1*pitchPacked
		
		else:
			yawPacked, pitchPacked = correctionList[(ipList[0]*2)-ipList[2]][(ipList[1]*2)-ipList[3]]
			yawPacked = -1*yawPacked
			pitchPacked = -1*pitchPacked

	if (printOut != 0):
		print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		print("                       Input\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
		print(f'Camera center coordinates are:\t\t   [{ipList[0]:4d},{ipList[1]:4d}]\n\n')
		print(f'Drone center coordinates are:\t\t   [{ipList[2]:4d},{ipList[3]:4d}]\n\n')
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		print("                       Output\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
		print(f'yawPacked:\t\t int: {yawPacked:4d}  \tbit:  {yawPacked:08b}')
		if (yawPacked<0):
			print(f'\t\t\t deg: {-(abs(yawPacked)%32):4d} \tspeed: {(floor(abs(yawPacked)/32)):7d}\n')
		else:
			print(f'\t\t\t deg: {(abs(yawPacked)%32):4d} \tspeed: {(floor(abs(yawPacked)/32)):7d}\n')
		print(f'pitchPacked:\t\t int: {pitchPacked:4d}  \tbit:  {pitchPacked:08b}')
		if (pitchPacked<0):
			print(f'\t\t\t deg: {-(abs(pitchPacked)%32):4d} \tspeed: {(floor(abs(pitchPacked)/32)):7d}\n')
		else:
			print(f'\t\t\t deg: {(abs(pitchPacked)%32):4d} \tspeed: {(floor(abs(pitchPacked)/32)):7d}\n')
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
	return yawPacked, pitchPacked



if __name__=="__main__":   

	ImProcOutput = [960,540,0,1079]	# Test Image Processing submodule output

	NumberOfSpeedSettings = 4 		# Number of speed settings the Sentry Unit has
	
	cameraFOV = 53					# Camera horizontal FoV
	
	timeOrSpace = 0 				# 0 is focus on time and 1 is focus on space
	printOut = 0 					# 0 is no print and 1 is printing


	# Arguments for testing
	parser = argparse.ArgumentParser()
	parser.add_argument("--space", action="store_true")
	parser.add_argument("--list", action="store_true")
	parser.add_argument("--print", action="store_true")
	args = parser.parse_args()
	


	if args.space:
		timeOrSpace = 1
	
	if args.print:
		printOut = 1

	if args.list:
		motorCorrection(ImProcOutput,cameraFOV,NumberOfSpeedSettings,0,timeOrSpace,printOut)
	else:
		with open('correctionList.pkl', 'rb') as f:
			correctionList = pickle.load(f)
		motorCorrection(ImProcOutput,cameraFOV,NumberOfSpeedSettings,correctionList,timeOrSpace,printOut)
	

