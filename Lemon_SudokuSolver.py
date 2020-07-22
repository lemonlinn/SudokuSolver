import pygame
import pygame.freetype
import numpy as np

# example input

valid_matrix = np.array([[0,1,0,0,0,0,0,9,0],
		[0,0,0,5,0,6,0,0,0],
		[0,0,3,4,0,2,0,1,0],
		[0,7,0,0,4,0,3,0,1],
		[0,3,0,0,0,0,4,6,0],
		[5,0,9,0,3,0,0,8,0],
		[0,5,7,0,0,0,0,0,0],
		[0,9,6,0,0,0,0,2,0],
		[2,0,0,0,0,0,5,0,0]])

invalid_matrix = np.array([[0,1,0,0,0,0,0,9,0],
		[0,0,0,5,0,6,0,0,0],
		[0,7,3,4,0,2,0,1,0],
		[0,7,0,0,4,0,3,0,1],
		[0,3,0,0,0,0,4,6,0],
		[5,0,9,0,3,0,0,8,0],
		[0,5,7,0,0,0,0,0,0],
		[0,9,6,0,0,0,0,2,2],
		[2,0,0,0,0,0,5,0,0]])

valid_knight = np.array([[0,0,4,0,0,0,9,0,0],
	[0,0,0,0,3,0,0,0,0],
	[8,0,0,0,0,0,0,0,5],
	[0,0,0,8,0,9,0,0,0],
	[0,9,0,0,5,0,0,1,0],
	[0,0,0,1,0,2,0,0,0],
	[5,0,0,0,0,0,0,0,2],
	[0,0,0,0,7,0,0,0,0],
	[0,0,1,0,0,0,6,0,0]])

invalid_queen = np.array([[1,0,0,0,0,0,0,0,9],
	[0,2,0,0,0,0,0,8,0],
	[0,0,3,0,0,0,7,0,0],
	[0,0,0,4,0,6,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,4,0,6,0,0,0],
	[0,0,3,0,0,0,7,0,0],
	[0,2,0,0,0,0,0,8,0],
	[1,0,0,0,0,0,0,0,9]])

# check if input is valid

def valid_input(matrix):
	validity = []
	for x in np.arange(0,9):
		# check rows
		row = matrix[x,:]
		if sum(row) != sum(set(row)):
			validity.append(1)
		else:
			validity.append(0)

		# check cols
		col = matrix[:,x]
		if sum(col) != sum(set(col)):
			validity.append(1)
		else:
			validity.append(0)

	# check boxes/blocks
	for i in np.arange(0,9,3):
		for j in np.arange(0,9,3):
			block = [item for sublist in matrix[i:i+3,j:j+3] for item in sublist]
			if sum(block) != sum(set(block)):
				validity.append(1)
			else:
				validity.append(0)

	#evaluate validity
	if sum(validity) > 0:
		return False
	else:
		return True

def valid_number(matrix, row, col, number):
	validity = []
		# check rows
	myrow = matrix[row,:]
	if number in myrow:
		validity.append(1)
	else:
		validity.append(0)

		# check cols
	mycol = matrix[:,col]
	if number in mycol:
		validity.append(1)
	else:
		validity.append(0)

	#check boxes/blocks
	for i in np.arange(0,9,3):
		for j in np.arange(0,9,3):
			if row >= i and row < i+3:
				if col >= j and col < j+3:
					block = [item for sublist in matrix[i:i+3,j:j+3] for item in sublist]
					if number in block:
						validity.append(1)
					else:
						validity.append(0)

	#evaluate validity
	if sum(validity) > 0:
		return False
	else:
		return True

# isolate black cells from givens
def find_zero(matrix):
	zero_loc = [0,0]
	for i,m in enumerate(matrix):
		for j,n in enumerate(m):
			if n == 0:
				zero_loc = [i,j]
				return (True, zero_loc)
			else:
				continue
	return (False, zero_loc)

# vanilla solve with backtracking
def solve_sudoku(matrix):
	v = 0
	ifzero, wherezero = find_zero(matrix)
	if not ifzero:
		return True

	r = wherezero[0]
	c = wherezero[1]

	while v == 0:
		if valid_input(matrix):
			for x in np.arange(1,10):
				if valid_number(matrix, r, c, x):
					matrix[r][c] = x
					if solve_sudoku(matrix):
						#print(matrix)
						return True
					matrix[r][c] = 0
			return False
		else:
			#print("Sucks to suck")
			#return True
			v = 1
			return False

# check if number is valid (knights move)
def knights_move(matrix, row, col, number):
	#if row-1 >= 0 and row-3 >=0 and row+1 <=8 and row+3 <=8
	knightsCells = []

	if row+1 <= 8 and col+3 <= 8:
		knightsCells.append(matrix[row+1, col+3])

	elif row-1 >= 0 and col+3 <= 8:
		knightsCells.append(matrix[row-1, col+3])

	elif row+1 <= 8 and col-3 >= 0:
		knightsCells.append(matrix[row+1, col-3])

	elif row-1 >= 0 and col-3 >= 0:
		knightsCells.append(matrix[row-1, col-3])

	elif row+3 <= 8 and col+1 <= 8:
		knightsCells.append(matrix[row+3, col+1])

	elif row-3 >= 0 and col+1 <= 8:
		knightsCells.append(matrix[row-3, col+1])

	elif row+3 <= 8 and col-1 >= 0:
		knightsCells.append(matrix[row+3, col-1])

	elif row-3 >= 0 and col-1 >= 0:
		knightsCells.append(matrix[row-3, col-1])

	if number in knightsCells:
		return False
	else:
		return True

def queens_move(matrix, row, col, number):
	queensCells = []
	cols_left = col
	cols_right = 8-col
	rows_up = row
	rows_down = 8-row
	
	# up and left
	if rows_up != 0 or cols_left != 0:
		for ru, cl in zip(np.arange(1, rows_up+1), np.arange(1, cols_left+1)):
			queensCells.append(matrix[row-ru, col-cl])

	# up and right
	if rows_up != 0 or cols_right != 8:
		for ru, cr in zip(np.arange(1, rows_up+1), np.arange(1, cols_right+1)):
			queensCells.append(matrix[row-ru, col+cr])

	# down and left
	if rows_down != 8 or cols_left != 0:
		for rd, cl in zip(np.arange(1, rows_down+1), np.arange(1, cols_left+1)):
			queensCells.append(matrix[row+rd, col-cl])

	# down and right
	if rows_down != 8 or cols_right != 8:
		for rd, cr in zip(np.arange(1, rows_down+1), np.arange(1, cols_right+1)):
			queensCells.append(matrix[row+rd, col+cr])

	if number in queensCells:
		return False
	else:
		return True



#test
# print(solve_sudoku(valid_matrix))
# print(valid_matrix)
# print(solve_sudoku(invalid_matrix))
# print(invalid_matrix)

#print(valid_input(valid_matrix))
#print(valid_input(invalid_matrix))

#print(valid_number(valid_matrix, 1, 7, 9))
#print(valid_number(valid_matrix, 0, 0, 3))
#print(valid_number(valid_matrix, 1, 7, 7))

#print(knights_move(valid_knight, 2, 1, 3))
#print(knights_move(valid_knight, 2, 1, 4))

print(queens_move(invalid_queen, 4, 4, 5))
#print(queens_move(invalid_queen, 6, 2, 5))
print(queens_move(invalid_queen, 4, 4, 6))
#print(queens_move(invalid_queen, 0, 0, 1))