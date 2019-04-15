from __future__ import print_function
import sys
from utilities import *


class Game:

	"""
	Attributes:
	board - array of Tiles (class), 8x8 grid of unique tiles
	white_player - Player (class)
	black_player - Player (class)
	turn - int
	en_passant - Tile (class), indicates which (if any) pawn is eligible to be captured en_passant
	mode - string, takes "standard", "test"
	log - 2x[turn] matrix of strings, records all moves made
	"""

	def set_board(self):
		self.board = []
		for i in range(8):
			self.board.append([])
			for j in range(8):
				self.board[i].append(Tile(j,i))
	
	def set_up_board(g):
		for i in range(8):
			for j in range(8):
				if i == 0:
					if j == 0 or j == 7:
						g.board[i][j].occupant = Piece("white", 'R')
					if j == 1 or j == 6:
						g.board[i][j].occupant = Piece("white", 'N')
					if j == 2 or j == 5:
						g.board[i][j].occupant = Piece("white", 'B')
					if j == 3:
						g.board[i][j].occupant = Piece("white", 'Q')
					if j == 4:
						g.board[i][j].occupant = Piece("white", 'K')
				if i == 1:
					g.board[i][j].occupant = Piece("white", 'P')
				if i == 6:
					g.board[i][j].occupant = Piece("black", 'P')
				if i == 7:
					if j == 0 or j == 7:
						g.board[i][j].occupant = Piece("black", 'R')
					if j == 1 or j == 6:
						g.board[i][j].occupant = Piece("black", 'N')
					if j == 2 or j == 5:
						g.board[i][j].occupant = Piece("black", 'B')
					if j == 3:
						g.board[i][j].occupant = Piece("black", 'Q')
					if j == 4:
						g.board[i][j].occupant = Piece("black", 'K')
		#print("board set up")

	def display_board(self):
		for i in range(8):
			for j in range(8):
				self.board[7-i][j].display()
				print("\t",end='')
			print('\n\n')

	def set_white_player(self):
		self.white_player = Player("white")

	def set_black_player(self):
		self.black_player = Player("black")

	def set_turn(self, n):
		self.turn = n

	def set_en_passant(self):
		self.en_passant = None

	def set_mode(self, s):
		self.mode = s

	def set_log(self, l):
		self.log = l

	def __init__(self):
		self.set_board()
		self.set_white_player()
		self.set_black_player()
		self.set_turn(1)
		self.set_en_passant()
		self.set_mode("unset")
		self.set_log([])

	def execute(self, m):

		c = m.from_tile.occupant
		if m.type == "normal":
			m.to_tile.occupant = c
			m.from_tile.occupant = None

			if m.real:
				#Remove castling ability if moved piece was king or rook
				if c.type == 'K':
					m.player.short_castle = False
					m.player.long_castle = False
				if c.type == 'R':
					if (m.player.color == "white" and m.from_tile.name() == "a1") or (m.player.color == "black" and m.from_tile.name() == "a8"):
						m.player.long_castle = False
					elif (m.player.color == "white" and m.from_tile.name() == "h1") or (m.player.color == "black" and m.from_tile.name() == "h8"):
						m.player.short_castle = False

				#Allow en_passant if move was double step
				if c.type == 'P' and abs(m.from_tile.y - m.to_tile.y) == 2:
					self.en_passant = m.to_tile
				else:
					self.en_passant = None

				#Make sure the move promoted if necessary
				if c.type == 'P' and (m.to_tile.y == 7 or m.to_tile.y == 0):
					call_error(5)

		elif "promotion" in m.type:

			if m.player.type == "human":
				d = Piece(c.color, m.type[len(m.type)-1])
				m.to_tile.occupant = d
				m.from_tile.occupant = None
				self.en_passant = None
			else:
				#print("exucting promotion for ", end='')
				m.display()
				m.to_tile.occupant = Piece(c.color, 'Q')
				m.from_tile.occupant = None
				self.en_passant = None

		elif m.type == "en passant":
			m.to_tile.occupant = c
			m.from_tile.occupant = None
			self.en_passant.occupant = None
			self.en_passant = None

		elif m.type == "castle":
			m.to_tile.occupant = c
			m.from_tile.occupant = None
			if m.to_tile.name() == "c1":
				self.board[0][3].occupant = self.board[0][0].occupant
				self.board[0][0].occupant = None
			if m.to_tile.name() == "g1":
				self.board[0][5].occupant = self.board[0][7].occupant
				self.board[0][7].occupant = None
			if m.to_tile.name() == "c8":
				self.board[7][3].occupant = self.board[7][0].occupant
				self.board[7][0].occupant = None
			if m.to_tile.name() == "g8":
				self.board[7][5].occupant = self.board[7][7].occupant
				self.board[7][7].occupant = None
			m.player.short_castle = False
			m.player.long_castle = False
			self.en_passant = None

		else:
			call_error(1)

	def clone(self):
		res = Game()
		for i in range(8):
			for j in range(8):
				if self.board[i][j].occupant != None:
					res.board[i][j].occupant = Piece(self.board[i][j].occupant.color, self.board[i][j].occupant.type)
		res.white_player = self.white_player.clone()
		res.black_player = self.black_player.clone()
		res.turn = self.turn
		res.mode = self.mode
		return res

	def display_log(self):
		i = 1
		for line in self.log:
			print(str(i) + ".", end='')
			for cell in line:
				print(cell + " ", end='')
			print("")
			i = i + 1

	def write_log(self):

		file_name = self.white_player.name + " vs " + self.black_player.name
		path = "Saved Games/" + file_name + ".chs"
		myfile = open(path, 'w')

		i = 1
		for line in self.log:
			myfile.write(str(i) + ".")
			for cell in line:
				myfile.write(cell + " ")
			myfile.write("\n")
			i = i + 1		


class Tile:

	"""
	Attributes:
	x - int, the horizontal (lettered) coordinate of the tile
	y - int, the vertical (numbered) coordinate of the tile
	occupant - Piece (class), the piece currently occupying this tile
	"""

	def set_x(self, x):
		self.x = x

	def set_y(self, y):
		self.y = y

	def set_occupant(self, o):
		self.occupant = o

	def __init__(self, x, y):
		self.set_x(x)
		self.set_y(y)
		self.set_occupant(None)

	def name(self):
		x_returns = {0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
		return x_returns[self.x] + str(self.y+1)

	def display(self):
		if self.occupant == None:
			print('0',end='')
		else:
			self.occupant.display()


class Piece:

	"""
	Attributes:
	color - string, takes "white", and "black"
	type - char, takes 'P','R','N','B','Q', and 'K'
	"""

	def set_color(self, c):
		self.color = c

	def set_type(self, t):
		self.type = t

	def __init__(self, c, t):
		self.set_color(c)
		self.set_type(t)

	def display(self):
		color_return = {"white":'w',"black":'b'}
		print(color_return[self.color]+self.type,end='')


class Player:

	"""
	Attributes:
	name - string, customized by player
	type - string, takes "human" and "computer"
	color - string, takes "white" and "black"
	short_castle - boolean
	long_castle - boolean
	"""

	def set_name(self, n):
		self.name = n

	def set_type(self, t):
		self.type = t

	def set_color(self, c):
		self.color = c

	def set_short_castle(self, b):
		self.short_castle = b

	def set_long_castle(self, b):
		self.long_castle = b

	def __init__(self, c):
		self.set_name("UNASSIGNED")
		self.set_type("UNASSIGNED")
		self.set_color(c)
		self.set_short_castle(True)
		self.set_long_castle(True)

	def display(self):
		print(self.color + " player:\n\t" + self.name + "\n\t" + self.type)
		if self.short_castle:
			print("\tcan castle short")
		else:
			print("\tcannot castle short")

		if self.long_castle:
			print("\tcan castle long")
		else:
			print("\tcannot castle long")

	def clone(self):
		res = Player(self.color)
		res.name = self.name
		res.type = self.type
		res.short_castle = self.short_castle
		res.long_castle = self.long_castle
		return res


class Move:

	"""
	Attributes:
	from_tile - Tile (class)
	to_tile - Tile (class)
	player - Player (class)
	type - string, takes "normal", "promotion", "en passant", and "castle"
	real - boolean, indicates whether the move is real or hypothetical (as in testing for check)
	score - double, indicates how promising a certain move is 
			(irrevelant for human players)
	"""

	def set_from_tile(self, t):
		self.from_tile = t

	def set_to_tile(self, t):
		self.to_tile = t

	def set_player(self, p):
		self.player = p

	def set_type(self, t):
		self.type = t

	def set_real(self, b):
		self.real = b

	def set_score(self, s):
		self.score = s

	def __init__(self, t1, t2, p, r):
		self.set_from_tile(t1)
		self.set_to_tile(t2)
		self.set_player(p)
		self.set_type("normal")
		self.set_real(r)
		self.set_score(0)

	def display(self):
		if self.from_tile.occupant == None:
			call_error(2)
		else:
			color_return = {"white":'w',"black":'b'}
			print(color_return[self.from_tile.occupant.color]
				+ self.from_tile.occupant.type + 
				" at " + self.from_tile.name() + " moves to "
				+ self.to_tile.name() + "\tscore: " + str(self.score))

	def clone(self, g):

		res_player = g.white_player
		if self.player.color == "black":
			res_player = g.black_player

		res = Move(g.board[self.from_tile.y][self.from_tile.x],
			g.board[self.to_tile.y][self.to_tile.x], res_player, self.real)
		res.score = self.score
		return res


class Tree:

	"""
	Attributes:
	parent - Move
	children - list of trees
	"""

	def set_parent(self, p):
		self.parent = p

	def set_children(self, c):
		self.children = c

	def __init__(self, p):
		self.set_parent(p)
		self.set_children([])

	def display(self):
		print("given parent ", end='')
		self.parent.display()
		print("possible continuations are...")
		for child in self.children:
			print("\t", end='')
			child.parent.display()

	def clone(self, g):
		res = Tree(self.parent.clone(g))
		for t in self.children:
			res.children.append(Tree(t.clone(g)))
		return res




















