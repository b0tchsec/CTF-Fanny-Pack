#!/usr/bin/env python
import math

############################################################
# Author: Aaron Gallagher <aaron.b.gallagher@gmail.com>
############################################################


def main():
	#Open the file, we will need to read the GPS data
	f = open('tracking.in', 'r')

	#throw out first 2 lines
	f.readline()
	f.readline()

	float_list = []

	#Parse the d_{1}, d_{2}, d_{3}, and d_{4} measurements for each
	#coordinate from the file
	for i in range(45):
		cont = f.readline().strip().split(' ')
		float_list.append((float(cont[0]),
			float(cont[1]),
			float(cont[2]),
			float(cont[3])))
	f.close()

	#Satellite Data (Manually extracted from tracking.in)
	p = 2000
	q = 2000
	r = 2000
	s = 3000
	t = 1500
	u = 1750

	#calculate the x,y,z position for each coordinate measurement
	x_list = []
	y_list = []
	z_list = []
	for d1,d2,d3,d4 in float_list:
		x = (d1**2 - d2**2 + p**2)/(2*p)
		y = ( (d1**2 - d3**2 + q**2 + r**2)/(2*r) ) - ((q/r)*x)
		z = math.sqrt(d1**2 - x**2 - y**2)
		x_list.append(x)
		y_list.append(y)
		z_list.append(z)

	#calculate x average
	xavg = 0
	for x in x_list:
		xavg = math.ceil(xavg + x)
	xavg = math.ceil(xavg / len(x_list))
	print('Average x: %d' % xavg)

	#calculate y average
	yavg = 0
	for y in y_list:
		yavg = math.ceil(yavg + y)
	yavg = math.ceil(yavg / len(y_list))
	print('Average y: %d' % yavg)

	#calculate z average
	zavg = 0
	for z in z_list:
		zavg = math.ceil(zavg + z)
	zavg = math.ceil(zavg / len(z_list))
	print('Average z: %d' % zavg)

	#print the final flag
	print('Flag: sctf{%d, %d, %d}' % (xavg, yavg, zavg))


main()
