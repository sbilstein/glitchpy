#!/usr/bin/python
from PIL import Image
import sys
import os
import math 
import socket
import time

port = 6668
host = "10.0.0.37"

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()



image = sys.argv[1]
base = Image.open(image)

base.load() # array indexable by x,y

(width, height) = base.size
previous = base.copy()

# set x y r g b
def sendPixel(x, y, r, g, b):
	msg = "set {0} {1} {2} {3} {4}".format(x,y,r,g,b)
	print msg
	try:
		
		s.sendto(msg, (host, port))
	except socket.error, msg:
		print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

def filename(step):
	return "out" + str(step).zfill(4) + ".png"

def blur(current, k, radius):
	for i in range(radius, width, radius*2):
		for nj in range( 0 - radius -3, height, radius*2):
			j = max(nj, 0)
			(r,g,b) = base.getpixel((i,j))
			angle = k * 2 * math.pi / radius
			currentColor = (r + int(69 * math.cos(angle)), g + int(69* math.sin(angle + math.pi)), b)
			for a in range(i -k, i +k):
				for b in range(j -k, j +k):
					if(b > height -1 or a > width - 1 or b < 0 or a < 0):
						continue
					else:	
						current.im.putpixel((a, b), currentColor)

# how to draw a heart
# in a x by x square, divide into 4 quadrants
# pick center color

# def heart(current, k, radius, baseImg):
# 	for i in range(radius, width, radius * 2): 
# 		for j in range(radius, height, radius * 2):
# 			(r,g,b) = baseImg.getpixel((i,j))
# 			# bottom left
# 			for a in range(i, int(i + radius - (k * .5))):
# 				for b in range(int(j  - radius + (k *.5)), j):
# 				# for b in range(a, j + a):
# 					# if(b > height -1 or a > width - 1):
# 						 # continue
# 					# else:
# 					current.im.putpixel((a,b), (r,g,b))


step = 1
# slow at first 
for f in range(5, 15, 2):
	currentImg = previous.copy()		
	blur(currentImg, f, 15)
	# heart(currentImg, f, 16, base)
	print("saving generation " + str(step))
	currentImg.save(filename(step))			
	previous = currentImg
	step +=1

for f in range(1,20):
	newImg = base.copy()
	if( f % 2 == 0):
		blur(newImg, 15, 15)
	else:	
		blur(newImg, 14, 15)
	print("saving generation " + str(step))
	newImg.save(filename(step))
	step += 1

	

currentImg = base.copy()
for f in range(5, 15, 2):	
	blur(currentImg, f, 15)
	# heart(currentImg, f, 16, base)
	print("saving generation " + str(step + f))
	currentImg.save(filename(step + 35 - f))
	previous = currentImg
	currentImg = previous.copy()



print("generating gif")
os.system("convert -size 80% -quality 60% out*.png out.gif")
print("All done")