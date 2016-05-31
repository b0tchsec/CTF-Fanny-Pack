#!/usr/bin/env python
from pwn import *

HOST = 'p.tjctf.org'
PORT = '8006'
GAME_CNT = 50


def getemptycheatsheet():
	cheatsheet = []
	for i in range(GAME_CNT):
		cheatsheet.append(['north', 'south', 'east', 'west'])
	return cheatsheet


def makemove(p, cheatsheet, round):
	gamedata = p.recvuntil('> ')
	print(gamedata)
	possiblemoves = cheatsheet[round]
	if len(possiblemoves) != 1:
		exitstr = gamedata.split('Exits: ')[1]
		print(possiblemoves)
		for i in possiblemoves:
			if i not in exitstr:
				print('Removing: %s' % i)
				possiblemoves.remove(i)
		cheatsheet[round] = possiblemoves
	answer = cheatsheet[round][0]
	print('Answer: ' + answer)
	p.sendline(answer)


def singleplay(p, answer):
	gamedata = p.recvuntil('> ')
	print(gamedata)
	p.sendline(answer)


def playgame():
	p = remote(HOST, PORT)

	#process title
	for i in range(6):
		p.recvline()

	steps = [
	'examine tree',
	'south',
	'examine paper',		#can't read it
	'south',				#mystery shack gift shop
	'examine rug',			#first part of flag
	'examine eyeballjar',
	'examine cashregister',
	'up',					#attic of mystery shack
	'west',
	'examine uvlight',		#allows us to read paper
	'east',
	'down',
	'north',
	'examine paper',		#last part of flag
	'north',
	'north',				#buildings east and west, also lamppost
	'examine lamppost',
	'west',					#building with part of flag and crypto
	'examine journal2',
	'east',
	'east',					#museum
	'east',					#exhibit hall
	'examine paintedeye',	#reveals stairs
	'down',					#go downstairs
	'examine book',			#must already have already read journal2
	'up',
	'west',
	'west',
	'south',
	'examine tree',			#We were give clue to go check the clearing again
	]

	for step in steps:
		print(p.recvuntil('> '))
		p.sendline(step)
	print(p.recvuntil('> '))

	print('Done')


def main():
	playgame()


if __name__ == "__main__":
	main()
