from __future__ import print_function
from utilities import *
from classes import *
import sys
import time

def legal_move(m, g, test_check):

	#print("\testing legality of ", end='')
	#m.display()

	p = m.from_tile.occupant
	d = distance(m.from_tile, m.to_tile)
	ptype = path_type(m.from_tile, m.to_tile)

	if m.to_tile.occupant != None and m.to_tile.occupant.color == m.player.color:
		if m.real:
			print("Invalid move: Tile occupied by player's own piece")
		return False

	if p.type != 'N' and not clear_path(m,g):
		if m.real:
			print("Invalid move: Path obstructed")
		return False

	if p.type == 'K':

		#print("IN KING BLOCK")

		if d > 1 and m.type != "castle":
			if m.real:
				print("Invalid move: Kings can only move one space unless castling")
			return False

		if m.type == "castle":
			if in_check(m.player, g):
				if m.real:
					print("Invalid move: Cannot castle out of check")
				return False
			if m.to_tile.x == 6 and not m.player.short_castle:
				if m.real:
					print("Invalid move: Player can no longer castle kingside")
				return False
			if m.to_tile.x == 3 and not m.player.long_castle:
				if m.real:
					print("Invalid move: Player can no longer castle queenside")
				return False

			if p.color == "white":
				if m.to_tile.name() == "c1":
					if g.board[0][1].occupant != None:
						if m.real:
							print("Invalid move: Castling path obstructed")
						return False
					if can_attack(g.black_player, g.board[0][3], g):
						if m.real:
							print("Invalid move: d1 is threatened")
						return False
				elif m.to_tile.name() == "g1":
					if can_attack(g.black_player, g.board[0][5], g):
						if m.real:
							print("Invalid move: f1 is threatened")
						return False
				else:
					if m.real:
						print("Invlaid move: Cannot castle to specified tile")
					return False
			else:
				if m.to_tile.name() == "c8":
					if g.board[7][1].occupant != None:
						if m.real:
							print("Invalid move: Castling path obstructed")
						return False
					if can_attack(g.white_player, g.board[7][3], g):
						if m.real:
							print("Invalid move: d8 is threatened")
						return False
				elif m.to_tile.name() == "g8":
					if can_attack(g.white_player, g.board[7][5], g):
						if m.real:
							print("Invalid move: f8 is threatened")
						return False
				else:
					if m.real:
						print("Invalid move: Cannot castle to specified tile")
					return False

	if p.type == 'Q':
		if ptype == "other":
			if m.real:
				print("Invalid move: Queen can only move along straight lines or diagonals")
			return False

	if p.type == "R":
		if ptype != "straight":
			if m.real:
				print("Invalid move: Rooks can only move along straight lines")
			return False

	if p.type == 'B':
		if ptype != "diagonal":
			if m.real:
				print("Invalid move: Bishops can only move along diagonals")
			return False

	if p.type == 'N':
		if ptype != "other" or d != 2:
			if m.real:
				print("Invalid move: Knights can only move in the 'L' shape")
			return False

	if p.type == 'P':

		ep = False
		if g.en_passant != None and m.to_tile.x == g.en_passant.x and m.to_tile.x != m.from_tile.x:
			if (m.player.color == "white" and m.to_tile.y - g.en_passant.y == 1) or (m.player.color == "black" and m.to_tile.y - g.en_passant.y == -1):
				ep = True

		if (m.player.color == "white" and m.to_tile.y - m.from_tile.y <= 0) or (m.player.color == "black" and m.to_tile.y - m.from_tile.y >= 0):
			if m.real:
				print("Invalid move: Pawns can only advance towards the opponent's side")
			return False

		if d == 2 and ((m.player.color == "white" and m.from_tile.y != 1) or (m.player.color == "black" and m.from_tile.y != 6)):
			if m.real:
				print("Invalid move: Pawns can only move two spaces if they haven't already been moved")
			return False

		if d == 2 and m.to_tile.x != m.from_tile.x:
			if m.real:
				print("Invalid move: If moving two spaces, pawns must move in a straight line")
			return False

		if d > 2:
			if m.real:
				print("Invalid move: Pawns can never move more than two spaces at a time")
			return False

		if m.to_tile.x == m.from_tile.x and m.to_tile.occupant != None:
			if m.real:
				print("Invalid move: Pawns can only capture diagonally")
			return False

		if ep == False and m.to_tile.x != m.from_tile.x and m.to_tile.occupant == None:
			if m.real:
				print("Invald move: Pawns can only move diagonally if capturing")
			return False
	
	if test_check:
		g1 = g.clone()
		m1 = m.clone(g1)
		g1.execute(m1)
		if in_check(m1.player, g1):
			if m.real:
				print("Invalid move: Results in check")
			return False

	return True
	

def distance(t1, t2):
	x_distance = abs(t1.x - t2.x)
	y_distance = abs(t1.y - t2.y)
	return max(x_distance, y_distance)


def path_type(t1, t2):
	if t1.x == t2.x or t1.y == t2.y:
		return "straight"
	if abs(t1.x - t2.x) == abs(t1.y - t2.y):
		return "diagonal"
	return "other"


def clear_path(m, g):
	t1 = m.from_tile
	t2 = m.to_tile
	res = []

	#print("testing clear_path from " + t1.name() + " to " + t2.name())

	if t1.x == t2.x:
		#print("Block 1")

		for i in range(min(t1.y,t2.y)+1, max(t1.y,t2.y)):
			#print(g.board[i][t1.x].name())
			if g.board[i][t1.x].occupant != None:
				return False
		return True

	if t1.y == t2.y:
		#print("Block 2")

		for i in range(min(t1.x, t2.x)+1, max(t1.x,t2.x)):
			#print(g.board[t1.y][i].name())
			if g.board[t1.y][i].occupant != None:
				return False
		return True

	if abs(t1.x - t2.x) == abs(t1.y - t2.y):
		#print("Block 3")

		if t1.x < t2.x and t1.y < t2.y:
			#print("Block 3A")
			for i in range(1, abs(t1.x-t2.x)):
				#print(g.board[t1.y + i][t1.x + i].name())
				if g.board[t1.y + i][t1.x + i].occupant != None:
					#g.board[t1.y+i][t1.x+i].display()
					return False
			return True

		if t1.x < t2.x and t1.y > t2.y:
			#print("Block 3B")
			for i in range(1, abs(t1.x-t2.x)):
				#print(g.board[t1.y - i][t1.x + i].name())
				if g.board[t1.y - i][t1.x + i].occupant != None:
					#g.board[t1.y - i][t1.x + i].display()
					#print("")
					return False
			return True

		if t1.x > t2.x and t1.y < t2.y:
			#print("Block 3C")
			for i in range(1, abs(t1.x-t2.x)):
				#print(g.board[t1.y + i][t1.x - i].name())
				if g.board[t1.y + i][t1.x - i].occupant != None:
					#g.board[t1.y + i][t1.x - i].display()
				#	print("")
					return False
			return True

		if t1.x > t2.x and t1.y > t2.y:
			#print("Block 3D")
			for i in range(1, abs(t1.x-t2.x)):
				#print(g.board[t1.y - i][t1.x - i].name())
				if g.board[t1.y - i][t1.x - i].occupant != None:
					#g.board[t1.y - i][t1.x - i].display()
					#print("")
					return False
			return True
	return True

def in_check(p, g):

	#print("IN IN_CHECK")

	opponent = g.white_player
	if p.color == "white":
		opponent = g.black_player
	return can_attack(opponent, find('K',p,g)[0], g)


def can_attack(p,t,g):

	from classes import Move

	if t == None:
		call_error(4)

	#print("IN CAN_ATTACK for " + p.color + " attacking " + t.name())

	for i in range(8):
		for j in range(8):
			if g.board[i][j] != t and g.board[i][j].occupant != None:
				t1 = g.board[i][j]
				if t1.occupant.color == p.color and legal_move(Move(t1, t, p, False), g, False):
					return True
	return False


def find(c,p,g):
	res = []
	for i in range(8):
		for j in range(8):
			if g.board[i][j].occupant != None and g.board[i][j].occupant.type == c and g.board[i][j].occupant.color == p.color:
				res.append(g.board[i][j])
	return res

def keep_playing(p, g, message):

	for i in range(8):
		for j in range(8):
			if g.board[i][j].occupant != None and g.board[i][j].occupant.color == p.color and can_move(p,g,g.board[i][j]):
				
				return True

	if message:
		if in_check(p,g):
			print(p.color + " player in checkmate")
		else:
			print("Stalemate")
			
	return False


def can_move(p, g, t):

	for i in range(8):
		for j in range(8):
			if legal_move(Move(t, g.board[i][j], p, False), g, True):
				return True

	return False


















