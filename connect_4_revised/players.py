import numpy as np
import random
import pygame
import math
from connect4 import connect4
import sys
import copy

class connect4Player(object):
	def __init__(self, position, seed=0, CVDMode=False):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)
		if CVDMode:
			global P1COLOR
			global P2COLOR
			P1COLOR = (227, 60, 239)
			P2COLOR = (0, 255, 0)

	def play(self, env: connect4, move_dict: dict) -> None:
		move_dict["move"] = -1

class humanConsole(connect4Player):
	'''
	Human player where input is collected from the console
	'''
	def play(self, env: connect4, move_dict: dict) -> None:
		move_dict['move'] = int(input('Select next move: '))
		while True:
			if int(move_dict['move']) >= 0 and int(move_dict['move']) <= 6 and env.topPosition[int(move_dict['move'])] >= 0:
				break
			move_dict['move'] = int(input('Index invalid. Select next move: '))

class humanGUI(connect4Player):
	'''
	Human player where input is collected from the GUI
	'''

	def play(self, env: connect4, move_dict: dict) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move_dict['move'] = col
					done = True

class randomAI(connect4Player):
	'''
	connect4Player that elects a random playable column as its move
	'''

	def play(self, env: connect4, move_dict: dict) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move_dict['move'] = random.choice(indices)

class stupidAI(connect4Player):
	'''
	connect4Player that will play the same strategy every time
	Tries to fill specific columns in a specific order 
	'''


	def play(self, env: connect4, move_dict: dict) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move_dict['move'] = 3
		elif 2 in indices:
			move_dict['move'] = 2
		elif 1 in indices:
			move_dict['move'] = 1
		elif 5 in indices:
			move_dict['move'] = 5
		elif 6 in indices:
			move_dict['move'] = 6
		else:
			move_dict['move'] = 0

class minimaxAI(connect4Player):
	'''
	This is where you will design a connect4Player that 
	implements the minimiax algorithm WITHOUT alpha-beta pruning
	'''

	def evaluationFunction(env: connect4) -> int:
		player = env.turnPlayer
		_,numCols = env.shape
		for col in range(0,numCols):
			pos = env.topPosition[col]
			# vertical
			count = 0
			for i in range(1,3):
				if env.board[col][pos-i] == player:
					count += 1
					if count >= 3:
						return 1000
				else:
					break				
			
			# horizontal
			count = 0
			for i in range(1,3):
				if env.board[col+i][pos] == player:
					count += 1
					if count >= 3:
						return 1000
				else:
					break
				
			for i in range(1,3):
				if env.board[col-i][pos] == player:
					count += 1
					if count >= 3:
						return 1000
				else:
					break
				
			#diagonal ascending
			count = 0
			for i in range(1,3):
				if env.board[col+i][pos+i] == player:
					count += 1
					if count >= 3:
						return 1000
				else:
					break
			for i in range(1,3):
				if env.board[col-i][pos-i] == player:
					count += 1
					if count >= 3:
						return 1000
				else:
					break

				
			#diagonal descending
			count = 0
			for i in range(1,3):
				if env.board[col+i][pos-i] == player:
					count += 1
					if count >= 3:
						return 1000
				else:
					break
			for i in range(1,3):
				if env.board[col-i][pos+i] == player:
					count += 1
					if count >= 3:
						return 1000
				else:
					break
		return 0
	
	def simulateMove(env: connect4, column, position):
		env.board[column][env.topPosition[column]] = env.turnPlayer
	
	def MAX(self, env: connect4, depth):
		if env.gameOver():
			return -np.inf
		if depth == 0:
			return self.evaluationFunction(env.board)
		possible = env.topPosition >= 0 # which columns have empty spaces
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		value = -np.inf
		for column in indices:
			envCopy = copy.deepcopy(env)
			self.simulateMove(envCopy, column, self.position)
			value = max(value, self.MIN(envCopy, depth-1))
		return value
		
	def MIN(self, env: connect4, depth):
		if env.gameOver():
			return np.inf
		if depth == 0:
			return self.evaluationFunction(env.board)
		possible = env.topPosition >= 0 # which columns have empty spaces
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		value = np.inf
		for column in indices:
			envCopy = copy.deepcopy(env)
			self.simulateMove(envCopy, column, self.position)
			value = max(value, self.MAX(envCopy, depth-1))
		return value


	def play(self, env: connect4, move_dict: dict) -> None:
		maxDepth = 2
		self.MAX(env, maxDepth)
		move_dict[:] = [3]
		print("I finished")

		


	



	

class alphaBetaAI(connect4Player):
	'''
	This is where you will design a connect4Player that 
	implements the minimiax algorithm WITH alpha-beta pruning
	'''
	
	def play(self, env: connect4, move_dict: dict) -> None:
		pass

# Defining Constants
SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
P1COLOR = (255,0,0)
P2COLOR = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




