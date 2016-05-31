#!/usr/bin/env python
import sha

# hashes for each piece of the torrent file
PIECE_HASHES = [
'546b05909706652891a87f7bfe385ae147f61f91',
'589e942e00a7dd64a273deb5041c7ce469f2bad7',
'b411d7823a3c4ee3773cafca1e36b8cfd26655ba',
'f437cb078acc7c6d79873462334a355eddeb9459',
'b504c843b2ef4c55c673be0b1daf3b12c5cf2fe8',
'0699989c219e1d7b336851c646e88a651859d081',
'd8273e2f4a7c0a59554544c6605cdd8b117848aa',
'f2daf7bf8c0100e8421f6a72dd8064cad674813a',
'd0cf1ef21f0ce65584e2453a3fb427f6591adca8',
'1116ef128bb637e2d69e9666bfe6d8a4ef9d2c13',
'408c28a2da80ef8bc57e580ac9ffc7f69b2a0e0e',
'f9fc27b9374ad1e3bf34fdbcec3a4fd632427fed',
'c387c982a132d05cbd5f88840aef2c8157740049',
'b3127725f678ca5b1038b1df45a06f2ff4e1f544',
]


def crack(shahash):
	for x in range(127):
		for y in range(127):
			attempt = chr(x) + chr(y)
			res = sha.new(attempt).hexdigest()
			if res == shahash:
				return attempt

	print('Failed: ' + shahash)


def main():
	flag = ''
	for i in PIECE_HASHES:
		flag += crack(i)
	print(flag)


main()
