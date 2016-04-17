#!/usr/bin/env python

import socket
import sys
import Image
import base64
from pwn import *

RED		= (255, 0, 0)
PURPLE 	= (128, 0, 128)
BLUE 	= (0, 0, 255)
GREEN 	= (0, 128, 0)
YELLOW 	= (255, 255, 0)
ORANGE 	= (255, 165, 0)

BLACK = (0, 0, 0)
WHITE = (255,255,255)

HOST = 'problems1.2016q1.sctf.io'
PORT = 50000
BUFF = 9024

def main():
	#verticode()
	vertinet()
	

def verticode():
	im = Image.open('code1.png')
	print(im.size)
	message = get_str_from_image(im)
	print(message)


def vertinet():
	result = ''
	filename = 'newfile.png'
	conn = remote(HOST, PORT)

	for i in range(1,201):
		data = conn.recvuntil('\'></img>')
		b64 = get_b64_str(data)
		write_b64_file(b64, filename)
		im = Image.open(filename)
		message = get_str_from_image(im)
		result += message
		print('%d) %s' % (i, message))
		conn.send(message)

	final = conn.recv()
	print(final)


def get_str_from_image(im):
	bound = im.size[1] / 12
	result = ''
	pos = 0
	for x in range(bound):
		# GET COLOR
		box = (0, pos*12, 168/2, pos*12+12)
		region = im.crop(box)
		col = region.getpixel((0,0))
		shift = get_color_shift(col)

		# GET BIT CODE
		bit_code = ''
		for i in range(1,8):
			box = (168/2, pos*12, 168, pos*12+12)
			region = im.crop(box)
			code = region.getpixel((i*11,0))
			if code == WHITE:
				bit_code += '0'
			elif code == BLACK:
				bit_code += '1'
			else:
				assert(False)
		numb = convert_binstr(bit_code)
		result += chr(numb-shift)
		pos += 1

	return result


def convert_binstr(b):
	result = 0
	if b[0] == '1':
		result += 2**6
	if b[1] == '1':
		result += 2**5
	if b[2] == '1':
		result += 2**4
	if b[3] == '1':
		result += 2**3
	if b[4] == '1':
		result += 2**2
	if b[5] == '1':
		result += 2**1
	if b[6] == '1':
		result += 2**0
	return result


def get_color_shift(p):
	if p == RED:
		return 0
	elif p == PURPLE:
		return 1
	elif p == BLUE:
		return 2
	elif p == GREEN:
		return 3
	elif p == YELLOW:
		return 4
	elif p == ORANGE:
		return 5


def get_b64_str(b):
	# trim front
	start = 'base64,'
	idx = b.index(start) + len(start)
	b = b[idx:]

	#trim back
	end = '\'></img>'
	result = b[:len(b) - len(end)]
	return result


def write_b64_file(b64, filename):
	f = open(filename, 'w')
	f.write(base64.b64decode(b64))
	f.close()


main()
