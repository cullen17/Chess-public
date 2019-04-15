from __future__ import print_function
import sys
import time
from classes import *
from utilities import *
from rules import *


prompt = "=> "


def get_game_mode():

	print("Select game type:")
	print("\t(1) standard")
	print("\t(2) test")
	print(prompt,end='')
	sys.stdout.flush()
	res = str_to_int(trim(sys.stdin.readline(16)))

	while res != 1 and res != 2:
		print("invalid input")
		print("Select game type:")
		print("\t(1) standard")
		print("\t(2) test")
		print(prompt,end='')
		sys.stdout.flush()
		res = str_to_int(trim(sys.stdin.readline(16)))

	mode_return = {1:"standard",2:"test"}
	return mode_return[res]

def get_players(g):

	print("Enter name for white player:")
	print(prompt,end='')
	sys.stdout.flush()
	res = trim(sys.stdin.readline(32))

	g.white_player.name = res

	print("Select player type:")
	print("\t(1) Human")
	print("\t(2) Computer")
	print(prompt,end='')
	sys.stdout.flush()
	res = str_to_int(trim(sys.stdin.readline(16)))

	while res != 1 and res != 2 and res != 3:
		print("invalid input")
		print("Select player type:")
		print("\t(1) Human")
		print("\t(2) Computer")
		print(prompt,end='')
		sys.stdout.flush()
		res = str_to_int(trim(sys.stdin.readline(16)))

	type_return = {1:"human",2:"ai1",3:"ai2"}
	g.white_player.type = type_return[res]

	print("Enter name for black player:")
	print(prompt,end='')
	sys.stdout.flush()
	res = trim(sys.stdin.readline(32))

	g.black_player.name = res

	print("Select player type:")
	print("\t(1) Human")
	print("\t(2) Computer")
	print(prompt,end='')
	sys.stdout.flush()
	res = str_to_int(trim(sys.stdin.readline(16)))

	while res != 1 and res != 2 and res != 3:
		print("invalid input")
		print("Select player type:")
		print("\t(1) Human")
		print("\t(2) Computer")
		print(prompt,end='')
		sys.stdout.flush()
		res = str_to_int(trim(sys.stdin.readline(16)))

	g.black_player.type = type_return[res]

def get_move(p, g):

	print(prompt,end='')
	sys.stdout.flush()
	res = trim(sys.stdin.readline(16))
	m = parse(p, g, res)

	while m == None or legal_move(m, g, True) == False:
		print(prompt,end='')
		sys.stdout.flush()
		res = trim(sys.stdin.readline(16))
		m = parse(p, g, res)

	return m

def get_test_file():
	print("Specify .chs test file (without file extension):")
	print(prompt,end='')
	sys.stdout.flush()
	file_name = trim(sys.stdin.readline(256))
	path = "Saved Games/" + file_name + ".chs"

	myfile = open(path, 'r')
	my_text = myfile.readlines()

	
	return text_to_log(my_text)


def ask_save_log(g):

	res = "unset"
	while res[0] != 'n' and res[0] != 'y':
		print("Would you like to save the game log? (y/n)")
		print(prompt,end='')
		sys.stdout.flush()
		res = trim(sys.stdin.readline(16))

	if res[0] == 'n':
		return

	#add a . if game ended on Black's turn
	if len(g.log[g.turn-2]) == 1:
		g.log[g.turn-1].append(".")

	g.write_log()
	return

def ask_analyze():
	res = "unset"
	while res[0] != 'n' and res[0] != 'y':
		print("Would you like to analyze this board? (y/n)")
		print(prompt,end='')
		sys.stdout.flush()
		res = trim(sys.stdin.readline(16))

	if res[0] == 'n':
		return False

	return True


def valid_command(s):
#valid command examines the input to see if it is a plausible command
#it does not make any determination about the legality of the proposed move 

	x_values = ['a','b','c','d','e','f','g','h']
	y_values = ['1','2','3','4','5','6','7','8']
	other_values = ['x','R','N','B','Q','K']

	#test castle
	if s == "0-0" or s == "0-0-0":
		#print("Castle")
		return True

	#test surrender
	if s == "QQ":
		return True
	
	#test promotion
	if '=' in s:
		prom_values = ['Q','R','B','N']
		if len(s) == 4:
			if s[0] in x_values and (s[1] == '1' or s[1] == '8') and s[2] == '=' and s[3] in prom_values:
				return True
			else:
				return False
		if len(s) == 6:
			if s[0] in x_values and s[1] == 'x' and s[2] in x_values and (s[3] == '1' or s[3] == '8') and s[4] == '=' and s[5] in prom_values:
				return True
			else:
				return False
		else:
			return False

	#test length
	if len(s) > 5:
		#print("Too Long")
		return False

	#character by character parameters (working backwards)
	i = 1
	while i <= len(s):

		#isolate the ith to last character in the string
		char = s[len(s)-i]
		#print("testing " + char)

		#last char
		if i == 1:
			if char not in y_values:
				#print("X1")
				return False
		#second to last char
		elif i == 2:
			if char not in x_values:
				#print("X2")
				return False
		#third to last char
		elif i == 3:
			if len(s) == 3:
				if char not in other_values:
					#print("X3")
					return False
			if len(s) == 4:
				if char not in x_values and char not in y_values and char not in other_values:
					#print("X4")
					return False
			if len(s) == 5:
				if char != 'x':
					#print("X4")
					return False
		#fourth to last char
		elif i == 4:
			if len(s) == 4:
				if char not in x_values and char not in other_values:
					#print("X5")
					return False
			if len(s) == 5:
				if char not in x_values and char not in y_values:
					#print("X6")
					return False
		else:
			if char not in other_values:
				#print("X7")
				return False
		i = i + 1

	return True
	

def parse(p, g, s):

	#print("parsing " + s)

	if valid_command(s) == False:
		return None

	#Deal with surrender
	if s == "QQ":
		surrender(p,g)

	#deal with castling
	if s[0] == '0':

		if p.color == "white":
			x_coord = 0
		else:
			x_coord = 7

		from_y_coord = 4
		if len(s) == 3:
			to_y_coord = 6
		else:
			to_y_coord = 2

		res = Move(g.board[x_coord][from_y_coord],g.board[x_coord][to_y_coord],p,True)
		res.type = "castle"

		return res


	#deal with promotion
	if '=' in s:
		res = parse(p,g,s[:-2])
		res.type = "promotion=" + s[len(s)-1]
		return res

	#Take last two characters as coordinates for to_tile
	x = s[len(s)-1]
	y = s[len(s)-2]
	char_to_coord = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
	x_coord = str_to_int(x) - 1
	y_coord = char_to_coord[y]
	t = g.board[x_coord][y_coord]

	#print(t.name())
	#identify type of piece by first character
	if s[0] == 'K' or s[0] == 'Q' or s[0] == 'B' or s[0] == 'N' or s[0] == 'R': 
		c = s[0]
	else:
		c = 'P'

	#generate a list of tiles with pieces of correct 
	#type that can move to to_tile

	tile_list = find_tile(p, g, c, t)
	
	#deal with en_passant
	if c == 'P' and t.occupant == None and g.en_passant != None and t.x == g.en_passant.x and ((p.color == "white" and t.y - g.en_passant.y == 1) or (p.color == "black" and t.y - g.en_passant.y == -1)):
		if len(tile_list) == 1:
			res = Move(tile_list[0], t, p, g)
			res.type = "en passant"
			return res
		else:
			for x in tile_list:
				if x.x == s[0]:
					res = Move(tile_list[0], t, p, g)
					res.type = "en passant"
					return res

	# for tile in tile_list:
	# 	print('\t' + tile.name() + ": ", end='')
	# 	tile.display()
	# 	print('')

	#print(c)
	#if only one tile in list, use it as from_tile
	#if two or more, then use the second char to ID correct tile
	#except for pawns, which require first char
	if len(tile_list) == 0:
		return None
	elif len(tile_list) == 1:
		return Move(tile_list[0], t, p, True)
	elif c == 'R' or c == 'N' or c == 'B' or c == 'Q':
		if len(s) != 4 and len(s) != 5:
			return None
		z = s[1]
		for tile in tile_list:
			if tile.name()[0] == z or tile.name()[1] == z:
				return Move(tile, t, p, True)
		return None
	elif c == 'P':
		for tile in tile_list:
			if tile.name()[0] == s[0]:
				return Move(tile, t, p, True)
		return None
	else:
		return None

def unparse(m, g):
	res = []
	c = m.from_tile.occupant.type
	player = m.player.color

	#Which piece is being moved?
	#If Castle, just return the standard castle strings
	if m.type == "castle":
		if m.to_tile.x == 2:
			return "O-O-O"
		else:
			return "O-O"
	#for non-pawns, add type character
	elif c != 'P':
		res.append(c)
	#for a pawn capture, add starting file
	elif m.to_tile.occupant != None or m.type == "en_passant":
		res.append(m.from_tile.name()[0])

	#Is the move ambiguous?
	tile_list = find_tile(m.player, g, c, m.to_tile)
	if len(tile_list) > 1:
		#If files are different, add starting file
		if tile_list[0].x != tile_list[1].x:
			res.append(m.from_tile.name()[0])
		#otherwise, add starting rank
		else:
			res.append(m.from_tile.name()[1])

	#Is the move a capture?
	if m.to_tile.occupant != None:
		res.append('x')

	#add destination tile name
	res.append(m.to_tile.name()[0])
	res.append(m.to_tile.name()[1])

	#Was a pawn promoted?
	if "promotion" in m.type:
		res.append(m.type[len(m.type)-2])
		res.append(m.type[len(m.type)-1])

	return "".join(res)

def find_tile(p, g, c, t):
	candidates = find(c,p,g)
	res = []
	for x in candidates:
		if legal_move(Move(x,t,p,False),g,False):
			res.append(x)
	return res

def record(g, m):
	if m.player.color == "white":
		g.log.append([])
	g.log[g.turn-1].append(unparse(m, g))

def text_to_log(s):
	i = 0
	skip = 2
	res = []
	cell = []
	header = 2

	for line in s:
		if i == 9:
			header = 3
		if i == 99:
			header = 4

		line = line[header:]
		res.append([])
		res[i].append(line.split()[0])
		res[i].append(line.split()[1])
		i = i+1

	return res

def surrender(p, g):
	print(p.name + " surrenders")
	end_game(g)

def end_game(g):
	ask_save_log(g)
	print("Thanks for playing!")
	exit()






