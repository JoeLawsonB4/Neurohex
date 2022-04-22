import numpy as np

white = 0
black = 1

def other(color):
	return not color

west = 2
east = 3
north = 4
south = 5
topBlack = 7
topRightBlack = 8
bottomRightBlack = 19
bottomBlack = 10
bottomLeftBlack = 11
topLeftBlack = 6
topWhite = 13 
topRightWhite = 14
bottomRightWhite = 15
bottomWhite = 16
bottomLeftWhite = 17
topLeftWhite = 12
num_channels = 18
boardsize = 13
padding = 2
input_size = boardsize+2*padding
neighbor_patterns = ((-1,0), (0,-1), (-1,1), (0,1), (1,0), (1,-1))
two_step_patterns = ((-1,-1), (1,-2), (2,-1), (1,1), (-1,2),(-2,1))

input_shape = (num_channels,input_size,input_size)

def cell(move):
	x =	ord(move[0].lower())-ord('a')+padding
	y = int(move[1:])-1+padding
	return (x,y)

def move(cell):
	return chr(ord('a')+cell[0]-padding)+str(cell[1]-padding+1)

#cell of the mirrored move
def cell_m(cell):
	return (cell[1],cell[0])

def neighbors(cell):
	"""
	Return list of neighbors of the passed cell.
	"""
	x = cell[0]
	y = cell[1]
	return [(n[0]+x , n[1]+y) for n in neighbor_patterns\
		if (0<=n[0]+x and n[0]+x<input_size and 0<=n[1]+y and n[1]+y<input_size)]

def twoStep(cell):
	"""
	Return list of twoStep neighbors of the passed cell.
	"""
	x = cell[0]
	y = cell[1]
	return [(n[0]+x , n[1]+y) for n in two_step_patterns\
		if (0<=n[0]+x and n[0]+x<input_size and 0<=n[1]+y and n[1]+y<input_size)]

def mirror_game(game):
	m_game = np.zeros(input_shape, dtype=bool)
	m_game[white]=np.transpose(game[black])
	m_game[black]=np.transpose(game[white])
	m_game[north]=np.transpose(game[west])
	m_game[east] =np.transpose(game[south])
	m_game[south]=np.transpose(game[east])
	m_game[west] =np.transpose(game[north])
	m_game[topBlack]=np.transpose(game[bottomLeftBlack])
	m_game[bottomLeftBlack]=np.transpose(game[topBlack])
	m_game[bottomBlack]=np.transpose(game[topRightBlack])
	m_game[topRightBlack] =np.transpose(game[bottomBlack])
	m_game[bottomRightBlack]=np.transpose(game[bottomRightBlack])
	m_game[topLeftBlack] =np.transpose(game[topLeftBlack])
	m_game[topWhite]=np.transpose(game[bottomLeftWhite])
	m_game[bottomLeftWhite]=np.transpose(game[topWhite])
	m_game[bottomWhite]=np.transpose(game[topRightWhite])
	m_game[topRightWhite] =np.transpose(game[bottomWhite])
	m_game[bottomRightWhite]=np.transpose(game[bottomRightWhite])
	m_game[topLeftWhite] =np.transpose(game[topLeftWhite])
	return m_game

def flip_game(game):
	m_game = np.zeros(input_shape, dtype=bool)
	m_game[white] = np.rot90(game[white],2)
	m_game[black] = np.rot90(game[black],2)
	m_game[north] = np.rot90(game[south],2)
	m_game[east]  = np.rot90(game[west],2)
	m_game[south] = np.rot90(game[north],2)
	m_game[west]  = np.rot90(game[east],2)
	m_game[topWhite] = np.rot90(game[bottomBlack],2)
	m_game[bottomWhite] = np.rot90(game[topBlack],2)
	m_game[topRightWhite] = np.rot90(game[bottomLeftWhite],2)
	m_game[topLeftWhite]  = np.rot90(game[bottomRightWhite],2)
	m_game[bottomRightWhite] = np.rot90(game[topLeftWhite],2)
	m_game[bottomLeftWhite]  = np.rot90(game[topRightWhite],2)
	return m_game

def new_game(size = boardsize):
	if(size > boardsize):
		raise(ValueError("Boardsize must be"+str(boardsize)+" or less"))
	even = 1 - size%2
	true_padding = int ((input_size - size+1)/2)
	game = np.zeros(input_shape, dtype=bool)
	game[white, 0:true_padding, :] = 1
	game[white, input_size-true_padding+even:, :] = 1
	game[west, 0:true_padding, :] = 1
	game[east, input_size-true_padding+even:, :] = 1
	game[black, :, 0:true_padding] = 1
	game[black, :, input_size-true_padding+even:] = 1
	game[north, :, 0:true_padding] = 1
	game[south, :, input_size-true_padding+even:] = 1

	return game

def winner(game):
	if(game[east,0,0] and game[west,0,0]):
		return white
	elif(game[north,0,0] and game[south,0,0]):
		return black
	return None

def flood_fill(game, cell, color, edge):
	game[edge, cell[0], cell[1]] = 1
	for n in neighbors(cell):
		if(game[color, n[0], n[1]] and not game[edge, n[0], n[1]]):
			flood_fill(game, n, color, edge)

def play_cell(game, cell, color):
	edge1_connection = False
	edge2_connection = False
	game[color, cell[0], cell[1]] = 1
	if(color == white):
		edge1 = east
		edge2 = west
		notColor = black
		notColorI = 6
		colorI = 12

	else:
		edge1 = north
		edge2 = south
		notColor = white
		notColorI = 12
		colorI = 6

	i = 0
	cellNeighbors = neighbors(cell)
	twoStepNeighbors = twoStep(cell)
	for n in cellNeighbors:
		if(game[edge1, n[0], n[1]] and game[color, n[0], n[1]]):
			edge1_connection = True
		if(game[edge2, n[0], n[1]] and game[color, n[0], n[1]]):
			edge2_connection = True
		if(game[color , twoStepNeighbors[i][0], twoStepNeighbors[i][1]] and (not game[notColor, n[0],n[1]]) and (not game[notColor, cellNeighbors[(i + 1)%6][0], cellNeighbors[(i + 1)%6][1]])) :
			game[i + colorI,cell[0],cell[1]] = 1
			game[(i +3)%6 + colorI,twoStepNeighbors[i][0],twoStepNeighbors[i][1]] = 1
		game[(i + 2)%6 + notColorI,n[0],n[1]] = 0
		game[(i + 3)%6 + notColorI,n[0],n[1]] = 0

	if(edge1_connection):
		flood_fill(game, cell, color, edge1)
	if(edge2_connection):
		flood_fill(game, cell, color, edge2)

def state_string(state):
	"""
	Print an ascii representation of the input.
	"""
	w = 'O'
	b = '@'
	empty = '.'
	end_color = '\033[0m'
	edge1_color = '\033[31m'
	edge2_color = '\033[32m'
	both_color =  '\033[33m'
	invalid = '#'
	ret = '\n'
	coord_size = len(str(boardsize))
	offset = 1
	ret+=' '*(offset+2)
	for x in range(input_size):
		if(x<padding or x>=boardsize+padding):
			ret+=' '*(offset*2+1)
		else:
			ret+=chr(ord('A')+(x-padding))+' '*offset*2
	ret+='\n'
	for y in range(input_size):
		if(y<padding or y>=boardsize+padding):
			ret+=' '*(offset*2+coord_size)
		else:
			ret+=str(y+1-padding)+' '*(offset*2+coord_size-len(str(y+1-padding)))
		for x in range(input_size):
			if(state[white, x, y] == 1):
				if(state[west, x, y] == 1 and state[east, x, y]):
					ret+=both_color
				elif(state[west, x,y]):
					ret+=edge1_color
				elif(state[east, x, y]):
					ret+=edge2_color
				if(state[black, x, y] == 1):
					ret+=invalid
				else:
					ret+=w
				ret+=end_color
			elif(state[black, x, y] == 1):
				if(state[north, x, y] == 1 and state[south, x, y]):
					ret+=both_color
				elif(state[north, x,y]):
					ret+=edge1_color
				elif(state[south, x, y]):
					ret+=edge2_color
				ret+=b
				ret+=end_color
			else:
				ret+=empty
			ret+=' '*offset*2
		ret+="\n"+' '*offset*(y+1)
	ret+=' '*(offset*2+1)+(' '*offset*2)*input_size

	return ret