#!/usr/bin/python
from PIL import Image
import sys
import os


image = sys.argv[1]
base = Image.open(image)

base.load() # array indexable by x,y

(width, height) = base.size
previous = base.copy()
for f in range(1, 10):
	current = previous.copy()
	for i in range(width):
		for j in range(height):
			if (i % f == 0 and j % f == 1):
				current.im.putpixel((i,j), (f*11,(250 - f * 11),66))
	current.save("out" + str(f).zfill(3) + ".png")			
	previous = current


# current.save("trump.png")
os.system("convert out*.png out.gif")
