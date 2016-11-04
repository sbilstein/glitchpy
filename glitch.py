#!/usr/bin/python
from PIL import Image
import sys
import os
import math
import time

image = sys.argv[1]
base = Image.open(image)

base.load() # array indexable by x,y

(width, height) = base.size
previous = base.copy()

def filename(step):
	return "out" + str(step).zfill(4) + ".png"

def blur(current, k, radius):
	for i in range(radius, width, radius*2):
		for nj in range( 0 - radius -3, height, radius*2):
			j = max(nj, 0)
			(r,g,b,a) = base.getpixel((i,j))
			angle = k * 2 * math.pi / radius
			currentColor = (r + int(69 * math.cos(angle)), g + int(69* math.sin(angle + math.pi)), b)
			for a in range(i -k, i +k):
				for b in range(j -k, j +k):
					if(b > height -1 or a > width - 1 or b < 0 or a < 0):
						continue
					else:
						current.im.putpixel((a, b), currentColor)


step = 1
# slow at first
for f in range(5, 15, 2):
	currentImg = previous.copy()
	blur(currentImg, f, 10)
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
