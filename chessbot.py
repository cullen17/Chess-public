from __future__ import print_function
import sys
import time
from classes import *
from utilities import *
from rules import *
from player_input import *
import random

def get_computer_move(p, g):
	#print("in get_zeusbot_moves for " + p.color)

	depth = 5
	breadth = 3

	if p.type == "ai2":
		depth = 3
		breadth = 8
	
	trees = build_trees(p, g, depth, breadth, 1)
	rescore(trees)

	#sort_and_show(trees, g, True)
	print()
	return choose_move(trees)
	
def score(m, p, g):
	piece_to_score = {'P':1,'B':3,'N':3,'Q':9,'R':5,'K':0}
	score = 0
	A = 0
	B = .2 #Center weight
	C = 1 #Check penalty
	D = .1 #King weight
	#E = .3 #Threatening weight
	F = .1 #Pawn advance weight
	if g.turn >= 40:
		F = .5
	G = .2 #Development weight
	H = 1 #Castling bonus




	g1 = g.clone()
	m1 = m.clone(g1)
	g1.execute(m1)

	o = g1.white_player
	if p.color == "white":
		o = g1.black_player

	if not keep_playing(o, g1, False):
		if in_check(o, g1):
			m.score = 1000
			return
		else:
			m.score = 0
			return

	if in_check(p, g1):
		score = score - C
	if in_check(o, g1):
		score = score + C

	if m.type == "castle":
		score = score + H

	for i in range(8):
		for j in range(8):
			if g1.board[i][j].occupant == None:
				continue

			c = g1.board[i][j].occupant
			if c.color == p.color:
				A = 1
			else:
				A = -1

			#Material
			score = score + A*piece_to_score[c.type]

			#center control
			if g1.turn <= 20:
				if g1.board[i][j].name() == "d4" or g1.board[i][j].name() == "d5" or g1.board[i][j].name() == "e4" or g1.board[i][j].name() == "e5":
					score = score + A*B*piece_to_score[c.type]

			#King position
			if g1.turn <= 40:
				if c.type == 'K':
					score = score + A*D*(min(abs(3-i), abs(i-4)) + min(abs(3-j), abs(j-4)))
					
			#Threatening
			# if g1.turn > 10:
			# 	if c.color == p.color:
			# 		if can_attack(o, g1.board[i][j], g1):
			# 			score = score - E*piece_to_score[c.type]
			# 	else:
			# 		if can_attack(p, g1.board[i][j], g1):
			# 			score = score + E*piece_to_score[c.type]

			#Advance Pawns
			if c.type == 'P':
				if c.color == "white":
					score = score + A*F*(j - 2)
				else:
					score = score + A*F*(7 - j)

			#Develop Pieces
			if g1.turn <= 30:
				if c.type == 'B':
					if p.color == "white" and g1.board[i][j].name() != "c1" and g1.board[i][j].name() != "f1":
						score = score + A*G*3
					elif p.color == "black" and g1.board[i][j].name() != "c8" and g1.board[i][j].name() != "f8":
						score = score + A*G*3

				if c.type == 'N':
					if p.color == "white" and g1.board[i][j].name() != "b1" and g1.board[i][j].name() != "g1":
						score = score + A*G*3
					elif p.color == "black" and g1.board[i][j].name() != "b8" and g1.board[i][j].name() != "g8":
						score = score + A*G*3

				if c.type == 'Q':
					if p.color == "white" and g1.board[i][j].name() != "d1":
						score = score + A*G*3
					elif p.color == "black" and g1.board[i][j].name() != "d8":
						score = score + A*G*3


	m.score = score
	return


def all_player_moves(p ,g):
	#print("in all_player_moves")

	res = []
	for i in range(8):
		for j in range(8):
			if g.board[i][j].occupant != None and g.board[i][j].occupant.color == p.color:
				res = res + all_piece_moves(p, g, g.board[i][j])

	#print("leaving all_player moves")
	return res

def all_piece_moves(p, g, t):
	#print("in all piece moves for " + t.name() + " (" + t.occupant.type + ")")

	res = []
	for i in range(8):
		for j in range(8):
			m = Move(t, g.board[i][j], p, False)
			set_type(m, g)
			if legal_move(m, g, True):
				#print("Appending...", end='')
				#m.display()
				res.append(m)
				score(m,p,g)
	#print("leaving all piece moves")
	return res

def build_trees(p, g, depth, breadth, level):

	#Indicate that computer is thinking by printng a period each time a new branch is created
	if level == 2:
		print(".",end='')
		sys.stdout.flush()

	#print("in build trees at level " + str(level))
	res = []
	if level > depth:
		return res

	if p.color == "white":
		opponent = g.black_player
	else:
		opponent = g.white_player

	if level == 1:
		moves = all_player_moves(p,g)
		for m in moves:
			if m.score == 1000:
				return [Tree(m)]
	else:
		moves = some_player_moves(p,g,breadth)

	for move in moves:
		t = Tree(move)
		g1 = g.clone()
		m1 = move.clone(g1)
		g1.execute(m1)
		t.children = build_trees(opponent, g1, depth, breadth, level+1)
		res.append(t)

	#print("leaving build_trees at level " + str(level) + " with...\n\t", end='')
	return res

def some_player_moves(p,g,breadth):
	moves = all_player_moves(p,g)
	if len(moves) <= breadth or breadth == -1:
		return moves

	res = []
	for i in range(breadth):
		best = moves[0]
		for move in moves:
			if move.score > best.score:
				best = move
		res.append(best)
		moves.remove(best)
	return res

def rescore(trees):
	if trees == []:
		return

	for t in trees:
		if t.children != []:
			rescore(t.children)
			# print("calling best_score for ",end='')
			# t.parent.display()
			t.parent.score = -1*best_score(t.children)


def best_score(trees):
	if trees == []:
		call_error(6)

	res = trees[0].parent.score
	for t in trees:
		if t.parent.score > res:
			res = t.parent.score

	return res

def show_path(t):
	t.parent.display()
	if t.children == []:
		return

	for t1 in t.children:
		if t1.parent.score == -1*t.parent.score:
			show_path(t1)
			return

def set_type(m, g):
	if m.from_tile.occupant.type == 'K' and m.from_tile.x == 4 and ((m.player.color == "white" and (m.to_tile.name() == "a3" or m.to_tile.name() == "a7")) or (m.player == "black" and (m.to_tile.name() == "h3" or m.to_tile.name() == "h7"))):
		m.type = "castle"

	if m.from_tile.occupant.type == 'P' and ((m.player.color == "white" and m.to_tile.y == 7) or (m.player.color == "black" and m.to_tile.y == 0)):
		m.type = "promotion"

	if g.en_passant != None and m.from_tile.occupant.type == 'P' and m.to_tile.x != m.from_tile.x and m.to_tile.occupant == None and m.to_tile.y == g.en_passant.y:
		m.type = "en_passant"

	return

def choose_move(trees):
	best = trees[0].parent.score
	for t in trees:
		if t.parent.score > best:
			best = t.parent.score

	candidates = []
	for t in trees:
		if t.parent.score == best:
			candidates.append(t.parent)
			#t.parent.display()

	if len(candidates) > 1:
		rand = random.randrange(len(candidates))
		return candidates[rand]

	#If there's only one optimal move, there's a 1 in 10 chance of choosing the second best move
	rand = random.randrange(10)
	#print(rand)
	if rand == 0 and len(trees) > 1:
		#print("Choosing sub-optimal")
		for t in trees:
			if t.parent == candidates[0]:
				trees.remove(t)
		return choose_move(trees)

	return candidates[0]

def sort_and_show(trees, g, init):
	#print("In SNS with length " + str(len(trees)))
	if init:
		trees1 = []
		for t in trees:
			trees1.append(t.clone(g))

		sort_and_show(trees1, g, False)
		return

	if len(trees) == 1:
		trees[0].parent.display()
		return

	best = trees[0]
	for t in trees:
		if t.parent.score > best.parent.score:
			best = t

	best.parent.display()
	trees.remove(best)
	sort_and_show(trees, g, False)
	return










