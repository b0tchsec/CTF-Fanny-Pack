#!/usr/bin/env python
from pwn import *
import time
import random

HOST = 'p.tjctf.org'
PORT = 8007


def lookintocrystalball():
	p = process('./crystalball')
	return p.recvline()


def playgame():
	p = remote(HOST, PORT)
	print(p.recvline())
	for i in range(100):
		try:
			ans = lookintocrystalball()
			time.sleep(1)	#nice and slow-like
			p.sendline(ans)
			p.recvuntil('Correct!\n')
		except:
			print('Failed at round: %d' % (i+1))
			return False

	print(p.recv())
	return True


def main():
	won = False
	while not won:
		time.sleep(random.random())
		won = playgame()
		if not won:
			return


if __name__ == "__main__":
	main()
