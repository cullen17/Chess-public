from __future__ import print_function
import sys
import time
from classes import *
from utilities import *
from rules import *
from player_input import *
from chessbot import *



def start_game():

	print("\nWelcome to Chess")
	print("This program is under development\n")


	#Initiate game class, get user input to define values
	#for players and game mode
	g = Game()
	g.set_up_board()
	g.set_mode("standard")

	if g.mode == "test":
		g.log = get_test_file()
		play_test(g)
		exit()

	get_players(g)


	#Define counter to track which player's turn it happening
	player = 1
	int_to_player = {1:g.white_player,0:g.black_player}


	while keep_playing(int_to_player[player], g, True):

		play_turn(int_to_player[player],g)
		#increment the turn counter only if the completed turn was for black
		g.turn = g.turn + 1 - player
		#switch the player counter
		player = 1 - player

	end_game(g)


def play_turn(p, g):

	player_to_char = {g.white_player:'w',g.black_player:'b'}
	print(g.turn, end='')
	print(player_to_char[p])
	g.display_board()

	if p.type == "human":
		m = get_move(p, g)
	else:
		m = get_computer_move(p,g)
	record(g,m)
	print(unparse(m,g))
	g.execute(m)

def play_test(g):
	
	player = 1
	int_to_player = {1:g.white_player,0:g.black_player}

	g.display_log()

	while keep_playing(int_to_player[player], g, True) and g.turn <= len(g.log):

		int_to_char = {1:'w',0:'b'}
		print(str(g.turn) + int_to_char[player] + '.', end='')
		print(g.log[g.turn-1][1-player])

		if g.log[g.turn-1][1-player] == ".":
			print("Game Complete")
			if ask_analyze():
				int_to_player[player].type = "computer"
				get_chessbot_move(int_to_player[player], g).display()
			return

		m = parse(int_to_player[player], g, g.log[g.turn-1][1-player])
		g.execute(m)

		g.display_board()

		#increment the turn counter only if the completed turn was for black
		g.turn = g.turn + 1 - player
		#switch the player counter
		player = 1 - player

	print("Game Complete")
	if ask_analyze():
		int_to_player[player].type = "computer"
		get_chessbot_move(int_to_player[player], g).display()
	return



start_game()










