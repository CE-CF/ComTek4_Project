""" Kilder
https://stackoverflow.com/questions/58469297/how-do-i-calculate-the-yaw-pitch-and-roll-of-a-point-in-3d
https://mathinsight.org/spherical_coordinates
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import misc
import math
from math import cos, atan2, degrees, sqrt, pow
import numpy as np

def magnitude(x,y,z):
	distance = current-new
	return distance

def getHeading(opposite, adjecent):
	outputRad = atan2(opposite, adjecent)
	outputDegree = degrees(outputRad)
	return outputRad, outputDegree

def getHypotenuse(x, y, z=0):
	hypotenuse = sqrt(pow(x,2)+pow(y,2)+pow(z,2))
	return hypotenuse

def getPitch(opposite, adjecent):
	outputRad = atan2(opposite, adjecent)
	outputDegree = degrees(outputRad)
	return outputRad, outputDegree

"""
We can draw a triangle that forms a 90 degree angle with the X-axis (red triangle) and then calculate that angle. Recall from trigonometry tan(angle) = opposite / adjacent, and solving for angle, we get angle = arctan(opposite / adjacent).

In this case "adjacent" is a known quantity (redAdjacent = x = 1), and "opposite" is known too (redOpposite = z = 3). Instead of using arctan to solve the equation though, we want to use atan2 since it'll handle all the different cases of x and y for us.
"""

"""
Instead of "yaw, pitch, roll", I'm going to use the conventions "heading, pitch, bank" as defined by 3D Math Primer for Graphics and Game Development by Fletcher Dunn. (https://www.amazon.com/dp/1568817231)
"""
imgMidCord = [0,0,0]

droneMidCord = [1,2]

avgCaptureDistance = 3

x,y,z = droneMidCord[0], droneMidCord[1], avgCaptureDistance

redAdjacent = x
redOpposite = z
headingRad, headingDegree = getHeading(redOpposite, redAdjacent)


"""
Finally we need to find the pitch. Similarly to what we did with the heading, we can flatten the the 3D space into 2D along the plane that contains these three points: (A) the origin (0,0,0), (B) our point (1,2,3), and (C) our point as it would project onto the XZ plane (1,0,3) (e.g. by setting 0 for the Y-value).

If we draw a triangle between all 3 of these points, you will notice that they form a right-triangle again (green triangle). We can simply calculate the angle using arctan2 again.

We already calculated the green hypotenuse in step 1 (i.e. the magnitude of our vector):
"""
greenHypotenuse = getHypotenuse(x, y, z=z)
greenOpposite = y


"""
The way to calculate the adjacent length of the green triangle is to notice that redHypotenuse == greenAdjacent, and we could find redHypotenuse using:
"""
redHypotenuse = getHypotenuse(redAdjacent, redOpposite)

greenAdjecent = redHypotenuse

pitchRad, pitchDegree = getPitch(greenOpposite, greenAdjecent)

print(f'Mid of image coordinates are: [{imgMidCord[0]},{imgMidCord[1]}]\n\n')
print(f'The drone in located at: [{droneMidCord[0]},{droneMidCord[1]}]\n\n')

print(f'Yaw in rad and degrees: {headingRad} and {headingDegree} \n\n')
print(f'Pitch in rad and degrees: {pitchRad} and {pitchDegree} \n\n')