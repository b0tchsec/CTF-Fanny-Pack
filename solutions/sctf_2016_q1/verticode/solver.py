import sys
import Image

RED		= (255, 0, 0)
PURPLE 	= (128, 0, 128)
BLUE 	= (0, 0, 255)
GREEN 	= (0, 128, 0)
YELLOW 	= (255, 255, 0)
ORANGE 	= (255, 165, 0)

BLACK = (0, 0, 0)
WHITE = (255,255,255)


def main():
	im = Image.open('code1.png')

	result = ''
	pos = 0
	for x in range(1075):
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

	print(result)

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

	print(b)
	print(result)
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

main()
