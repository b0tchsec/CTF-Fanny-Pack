#!/usr/bin/env python

#####################################################################
# Failed Solution!!
#	-I think it was a networking bug, I appeared to be beating
#	the opponent until reading from the TCP socket would hang...
#
# Author: Aaron Gallagher <aaron.b.gallagher@gmail.com>
#####################################################################

"""

Tic-Tac-Toe

An important step towards the strong AI is the ability of an artificial agent to solve a well-defined problem. A project by the name 'tic-tac-toe' was one of such test problems. It's still up...

nc tic-tac-toe.2016.volgactf.ru 45679




The match is played over 500 rounds, the winner of each round gets 1.0 points, the looser gets 0.0 points, and in case of a draw each player gets 0.5 points.
To make your move choose the empty cell and send it's index followed by '\n', e.g. '4\n'.The indices map:
 0 | 1 | 2 
---+---+---
 3 | 4 | 5 
---+---+---
 6 | 7 | 8 

Round number 1.
Server vs. b0tch_sec. Current score: 0.0 - 0.0
   |   |   
---+---+---
   | X |   
---+---+---
   |   |   




"""

from random import randint
import socket
import time
import sys

HOST = 'tic-tac-toe.2016.volgactf.ru'
PORT = 45679
BUFFER_SIZE = 1024

MY_NAME = 'b0tch_sec'
BOARD = """ X |   | X 
---+---+---
   | X |   
---+---+---
   | O | O """
#BOARD_SIZE = len(BOARD)-2
BOARD_SIZE = 50

def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	# Please name yourself
	rx = s.recv(BUFFER_SIZE)
	print rx
	s.send(MY_NAME + '\n')

	# Get HELP message
	rx_help = s.recv(BUFFER_SIZE)
	print 'HELP:::\n' + rx_help

	# Play first round
	play_round(s)

	# end code
	s.close()
	print('END')


def play_round(s):
	#init game board
	game = tic_game(s)

	# play my first turn
	play_turn(game)

	# play my second turn
	play_turn(game)

	# play my third turn
	play_turn(game)

	while(True):
		play_turn(game)


def play_turn(game):
	#check if i am 1 way from winning, if so, play that move
	if game.choose_for_win(game.my_symbol):
		print('Win performed!')
		return

	#check if enemy is 1 away anywhere, if so, block that move
	if game.choose_for_win(game.enemy_symbol):
		print('Enemy win blocked!')
		return

	print('Making a random move')
	game.make_random_move()
	print('Random move completed...')


def readline(s):
	data = ''
	while '\n' not in data:
		data += s.recv(1)
		#sys.stdout.write(data)
		#sys.stdout.flush()
		#time.sleep(.25)
	return data

class tic_game():
	X = 'X'
	O = 'O'
	AVAIL = ' '

	def __init__(self, s):
		self.s = s
		self.update_game_state()

	def player_detection(self):
		#detect what symbol each player is
		#first player is X
		#second player is O
		self.my_symbol = 'O' if 'X' in self.curr_board_raw else 'X'
		self.enemy_symbol = 'X' if self.my_symbol == 'O' else 'O'
		print 'MY SYMBOL:::  ' + self.my_symbol

	def update_game_state(self):
		# Get raw data
		self.curr_board_raw = ''
		while True:
			#self.curr_board_raw += self.s.recv(BUFFER_SIZE)
			line = readline(self.s)
			if len(line) < 2:
				break
			self.curr_board_raw += line
		print 'RAW_DATA ::::::::\n' + self.curr_board_raw

		# Detect new game
		if 'Round number' in self.curr_board_raw:
			self.player_detection()

		# Update board layout state
		self.bl = board_layout(self.curr_board_raw)

		# Detect a full scoreboard
		open_spots = self.bl.get_open_spots()
		if len(open_spots)==0:
			#refresh the game state again
			self.update_game_state()

	def make_move(self, num):
		#make the move
		print('Performing move....:::::::::::%d' % num)
		self.s.send('%d\n' % num)

		#update the internal game board state
		self.update_game_state()

		#sleepy
		time.sleep(.2)

	def make_random_move(self):
		#get available spots
		open_spots = self.bl.get_open_spots()
		assert(len(open_spots)>0)

		#generate a random integer from open spots
		move_num = randint(0, len(open_spots)-1)

		#make the move from the open spots list
		self.make_move(open_spots[move_num])

	def choose_for_win(self, symbol):
		if self.choose_diagnol_win(symbol):
			print ('Choice made!!!')
			return True

		if self.choose_horizontal_win(symbol):
			print ('Choice made!!!')
			return True

		if self.choose_vertical_win(symbol):
			print ('Choice made!!!')
			return True

		print('No choices were made')
		return False

	def choose_diagnol_win(self, symbol):
		#check center
		if self.bl.test(4, symbol):
			#center is chosen, look for any one of the four corners
			if self.bl.test(0, symbol) and self.bl.test(8, tic_game.AVAIL):
				self.make_move(8)
				return True
			if self.bl.test(2, symbol) and self.bl.test(6, tic_game.AVAIL):
				self.make_move(6)
				return True
			if self.bl.test(6, symbol) and self.bl.test(2, tic_game.AVAIL):
				self.make_move(2)
				return True
			if self.bl.test(8, symbol) and self.bl.test(0, tic_game.AVAIL):
				self.make_move(0)
				return True

		#check top left, bottom right
		#or top right bottom left
		if ( self.bl.test(0, symbol) and self.bl.test(8, symbol) ) or \
		( self.bl.test(2, symbol) and self.bl.test(6, symbol) ):
			if self.bl.test(4, tic_game.AVAIL):
				#pick the center one for win!
				self.make_move(4)
				return True

		#no possible diagnol win
		return False

	def choose_horizontal_win(self, symbol):
		########Row 1
		#check top left, top right
		if self.bl.test(0, symbol) and self.bl.test(2, symbol) \
		and self.bl.test(1, tic_game.AVAIL):
			#pick the top center one for win!
			self.make_move(1)
			return True
		#check top left, top middle
		if self.bl.test(0, symbol) and self.bl.test(1, symbol) \
		and self.bl.test(2, tic_game.AVAIL):
			#pick top right for win
			self.make_move(2)
			return True
		#check top middle, top right
		if self.bl.test(1, symbol) and self.bl.test(2, symbol) \
		and self.bl.test(0, tic_game.AVAIL):
			#pick top left for win
			self.make_move(0)
			return True

		########Row 2
		#check middle left, middle right
		if self.bl.test(3, symbol) and self.bl.test(5, symbol) \
		and self.bl.test(4, tic_game.AVAIL):
			#pick the center one for win!
			self.make_move(4)
			return True
		#check middle left, center
		if self.bl.test(3, symbol) and self.bl.test(4, symbol) \
		and self.bl.test(5, tic_game.AVAIL):
			#pick the middle right for win
			self.make_move(5)
			return True
		#check center, middle right
		if self.bl.test(4, symbol) and self.bl.test(5, symbol) \
		and self.bl.test(3, tic_game.AVAIL):
			#pick the middle left for win
			self.make_move(3)
			return True

		########Row 3
		#check bottom left, bottom right
		if self.bl.test(6, symbol) and self.bl.test(8, symbol) \
		and self.bl.test(7, tic_game.AVAIL):
			#pick the bottom center one for win!
			self.make_move(7)
			return True
		#check bottom left, bottom middle
		if self.bl.test(6, symbol) and self.bl.test(7, symbol) \
		and self.bl.test(8, tic_game.AVAIL):
			#pick the bottom right for win
			self.make_move(8)
			return True
		#check bottom middle, bottom right
		if self.bl.test(7, symbol) and self.bl.test(8, symbol) \
		and self.bl.test(6, tic_game.AVAIL):
			#pick the bottom left for win
			self.make_move(6)
			return True

		#no possible diagnol win
		return False


	def choose_vertical_win(self, symbol):
		########Aisle 1
		#check top left, bottom left
		if self.bl.test(0, symbol) and self.bl.test(6, symbol) \
		and self.bl.test(3, tic_game.AVAIL):
			#pick the middle left for win
			self.make_move(3)
			return True
		#check top left, middle left
		if self.bl.test(0, symbol) and self.bl.test(3, symbol) \
		and self.bl.test(6, tic_game.AVAIL):
			#pick the bottom left for win
			self.make_move(6)
			return True
		#check middle left, bottom left
		if self.bl.test(3, symbol) and self.bl.test(6, symbol) \
		and self.bl.test(0, tic_game.AVAIL):
			#pick the top left for win
			self.make_move(0)
			return True

		########Aisle 2
		#check top middle, bottom middle
		if self.bl.test(1, symbol) and self.bl.test(7, symbol) \
		and self.bl.test(4, tic_game.AVAIL):
			#pick the center for win
			self.make_move(4)
			return True
		#check top middle, center
		if self.bl.test(1, symbol) and self.bl.test(4, symbol) \
		and self.bl.test(7, tic_game.AVAIL):
			#pick the bottom middle for win
			self.make_move(7)
			return True
		#check center, bottom middle
		if self.bl.test(4, symbol) and self.bl.test(7, symbol) \
		and self.bl.test(1, tic_game.AVAIL):
			#pick the top middle for win
			self.make_move(1)
			return True

		########Aisle 3
		#check top right, bottom right
		if self.bl.test(2, symbol) and self.bl.test(8, symbol) \
		and self.bl.test(5, tic_game.AVAIL):
			self.make_move(5)
			return True
		#check top right, middle right
		if self.bl.test(2, symbol) and self.bl.test(5, symbol) \
		and self.bl.test(8, tic_game.AVAIL):
			self.make_move(8)
			return True
		#check middle right, bottom right
		if self.bl.test(5, symbol) and self.bl.test(8, symbol) \
		and self.bl.test(2, tic_game.AVAIL):
			#pick the top right for win
			self.make_move(2)
			return True

		return False


#rawww   |   |    
class board_layout():
	def __init__(self, raw_txt):
		self.pos_table = []
		for i in range(9):
			self.pos_table += tic_game.AVAIL
		print(self.pos_table)

		# get start position
		#max_pos = len(raw_txt)
		#raw_pos = raw_txt.index('|') - 3
		#numb = 0

		# build pos list
		total_cnt = 0
		row_cntr = 0
		while total_cnt < 9:
			if row_cntr==0 or row_cntr==1:
				#trim off everything before first ocurrance of divider
				raw_pos = raw_txt.index('|') - 3
				raw_txt = raw_txt[raw_pos:]
				row_cntr += 1
			else:
				row_cntr = 0

			#add the character to the pos table
			if 'X' in raw_txt[:4]:
				self.pos_table[total_cnt] = tic_game.X
			elif 'O' in raw_txt[:4]:
				self.pos_table[total_cnt] = tic_game.O
			else:
				self.pos_table[total_cnt] = tic_game.AVAIL
			total_cnt += 1

			#trim the characters we just added off of the table
			raw_txt = raw_txt[4:]

		# debug print the table
		print(self.pos_table)
		# error check for first round
		assert(len(self.pos_table)==9)

	def get_open_spots(self):
		avail_list = []
		i = 0
		while i < len(self.pos_table):
			print('Position: %d, Contents: %s' % (i, self.pos_table[i]))
			if tic_game.X in self.pos_table[i]:
				pass
			elif tic_game.O in self.pos_table[i]:
				pass
			else:
				avail_list.append(i)
			i += 1

		print('available spots::')
		print(avail_list)
		print('number of available spots %d' % len(avail_list))
		return avail_list

	def test(self, numb, symbol):
		if symbol == tic_game.AVAIL:
			if 'X' in self.pos_table[numb] or 'O' in self.pos_table[numb]:
				return False
			else:
				return True
		if symbol in self.pos_table[numb]:
			return True
		return False

class GAMEOVER(Exception):
	def __init__(self,*args,**kwargs):
		Exception.__init__(self,*args,**kwargs)


main()
