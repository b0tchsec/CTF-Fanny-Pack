#!/usr/bin/python
# Simple but secure flag generator for ASIS CTF

from os import urandom
from hashlib import md5

l = 128
rd = urandom(l)
h = md5(rd).hexdigest()
flag = 'ASIS{' + h + '}'
f = open('flag.txt', 'r').read()
flag = ''
for c in f:
	code = hex(pow(ord(c), 65537, 143))[2:]
	print('%s => %s' % (c,code))
	flag += code
print flag
