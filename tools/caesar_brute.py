#!/usr/bin/env python
import sys

def doTheThing(offset, fname):
	dump = ''
	f = open(fname, 'rb')

	c = f.read(1)

	while c != '':
		i = ord(c)
		new = i + offset
		if new > 255:
			new = new - 256
		dump += chr(new)
		c = f.read(1)

	f.close()
	if sys.argv[2] in dump:
		print dump[dump.index(sys.argv[2]):dump.index(sys.argv[2])+50]
		print "Shift: " + str(offset)

def main():
	offset = 0x00
	fname = sys.argv[1]
	while offset < 0xff:
		doTheThing(offset, fname)
		offset += 0x01

if __name__ == "__main__":
	main()
