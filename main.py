EMPTY_BOARD = [["" for _ in range(8)] for _ in range(8)]

WHITE_KING = '♚'
WHITE_QUEEN = '♛'
WHITE_BISHOP = '♝'
WHITE_KNIGHT = '♞'
WHITE_ROOK = '♜'
WHITE_PAWN = '♟'
WHITE_PIECES = [WHITE_KING, WHITE_QUEEN, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK, WHITE_PAWN]

BLACK_KING = '♔'
BLACK_QUEEN = '♕'
BLACK_BISHOP = '♗'
BLACK_KNIGHT = '♘'
BLACK_ROOK = '♖'
BLACK_PAWN = '♙'
BLACK_PIECES = [BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK, BLACK_PAWN]



def main():
	print("welcome to clichess")
	input("press enter to start")
	board: list[list[str]] = starting_board()
	while True:
		draw(board)
		user_input: str = input(">> ")
		if user_input.lower() == 'quit':
			print("bye!")
			break
		board = process_input(board=board, user_input=user_input)

def starting_board():
	board = EMPTY_BOARD
	# pawns
	for i in range(8):
		board[1][i] = BLACK_PAWN
		board[6][i] = WHITE_PAWN
	# rooks
	for i in range(2):
		for j in range(2):
			is_white = i == 1
			y = i * 7
			x = j * 7
			rook = WHITE_ROOK if is_white else BLACK_ROOK
			board[y][x] = rook
	
	# knights
	for i in range(2):
		for j in range(2):
			is_white = i == 1
			y = i * 7
			x = j * 5 + 1
			knight = WHITE_KNIGHT if is_white else BLACK_KNIGHT
			board[y][x] = knight
	# bishops
	for i in range(2):
		for j in range(2):
			is_white = i == 1
			y = i * 7
			x = j * 3 + 2
			bishop = WHITE_BISHOP if is_white else BLACK_BISHOP
			board[y][x] = bishop
	# kings
	board[0][4] = BLACK_KING
	board[7][4] = WHITE_KING
	# queens
	board[0][3] = BLACK_QUEEN
	board[7][3] = WHITE_QUEEN
	return board

def draw(
	board: list[list[str]],
) -> None:
	output = "\n"
	output += "     a    b    c    d    e    f    g    h   \n"
	output += "   ________________________________________   \n"
	is_light = True
	for y_idx, row in enumerate(board):
		row_num = 8 - y_idx
		if is_light:
			output += "  |#####     #####     #####     #####     |  \n"
		else:
			output += "  |     #####     #####     #####     #####|  \n"
		for x_idx, piece in enumerate(row):
			if x_idx == 0:
				output += f"{row_num} |"
			if is_light:
				if piece:
					output += f"# {piece} #"
				else:
					output += "#####"
				
			else:
				if piece:
					output += f"  {piece}  "
				else:
					output += "     "
			if x_idx == 7:
				output += f"|  {row_num}"
			is_light = not is_light
		output += "\n"
		is_last_row = y_idx == 7
		empty_space = "_____" if is_last_row else "     "
		if is_light:
			output += f"  |#####{empty_space}#####{empty_space}#####{empty_space}#####{empty_space}|  \n"
		else:
			output += f"  |{empty_space}#####{empty_space}#####{empty_space}#####{empty_space}#####|  \n"
		is_light = not is_light
	output += "\n     a    b    c    d    e    f    g    h   \n"
	print(output)

def process_input(
	board,
	user_input : str,
) -> str:
	piece = user_input[0].upper()

	start_square = user_input[1:3]
	start_file = ord(start_square[0]) - ord('a')
	assert start_file >= 0 and start_file < 8
	start_rank = 7 - (int(start_square[1]) - 1)
	assert start_rank >= 0 and start_rank < 8

	end_square = user_input[3:5]
	end_file = ord(end_square[0]) - ord('a')
	assert end_file >= 0 and start_file < 8
	end_rank = 7 - (int(end_square[1]) - 1)
	assert end_rank >= 0 and end_rank < 8

	assert start_square != end_square

	is_valid_move: bool = is_valid(
		board=board,
		piece=piece,
		start_file=start_file,
		start_rank=start_rank,
		end_file=end_file,
		end_rank=end_rank,
	)
	if is_valid_move:
		board[start_rank][start_file] = ''
		board[end_rank][end_file] = get_piece_char(piece, is_white=True)
	else:
		print("Invalid move.")
	return board


def is_valid(
	board: list[list[str]],
	piece: str,
	start_file: int,
	start_rank: int,
	end_file: int,
	end_rank: int,
) -> bool:
	print(f"piece={piece}, start_rank={start_rank},start_file={start_file} end_rank={end_rank},end_file={end_file}")
	try:
		end_piece = board[end_rank][end_file]
		assert end_piece not in WHITE_PIECES, "cannot move there, a piece is in the way"
		is_end_empty = not end_piece
		if piece == 'P':
			forward = -1
			if is_end_empty:
				assert start_file == end_file, "pawns must move vertically, unless capturing"
				if end_rank == start_rank + forward:
					return True
				elif end_rank == start_rank + 2 * forward and start_rank == 6:
					is_path_empty = not board[end_rank + forward][end_file]
					assert is_path_empty, "the pawn's path is blocked"
					return True
				else:
					assert False, "pawns can only move forward"
			else:
				assert (end_file == start_file + 1 or end_file == start_file - 1), "pawns can only capture diagonally"
				assert (end_rank == start_rank + forward), "pawns can only move forward"
				return True
		elif piece == 'K':
			assert abs(start_file - end_file) <= 1 and abs(start_rank - end_rank) <= 1, "king can only move one square in any direction"
			return True
		elif piece == 'N':
			assert abs(start_file - end_file) <= 2 and abs(start_rank - end_rank) <= 2, "knights cannot move that far"
			assert abs(start_file - end_file) + abs(start_rank - end_rank) == 3, "knights must move in an L shape"
			return True
		elif piece == 'B':
			assert abs(start_file - end_file) == abs(start_rank - end_rank), "bishops can only move diagonally"
			distance = abs(start_file - end_file)
			direction_horizontal = int((end_file - start_file) / abs(end_file - start_file))
			direction_vertical = int((end_rank - start_rank) / abs(end_rank - start_rank))
			for i in range(1, distance):
				assert not board[start_rank + i * direction_vertical][start_file + i * direction_horizontal], "cannot move there, a piece is in the way"
			return True
		elif piece == 'R':
			assert (start_file == end_file and start_rank != end_rank) or (start_rank == end_rank and start_file != end_file), "rooks can only move horizontally or vertically"
			distance_horizontal = end_file - start_file
			direction_horizontal = 0 if distance_horizontal == 0 else int(distance_horizontal / abs(end_file - start_file))
			distance_vertical = end_rank - start_rank
			direction_vertical = 0 if distance_vertical == 0 else int(distance_vertical / abs(end_rank - start_rank))
			distance = max(abs(distance_horizontal), abs(distance_vertical))
			for i in range(1, distance):
				piece = board[start_rank + i * direction_vertical][start_file + i * direction_horizontal]
				assert not piece, "cannot move there, a piece is in the way"
			return True
		elif piece == 'Q':
			if abs(start_file - end_file) == abs(start_rank - end_rank): # move like a bishop
				distance = abs(start_file - end_file)
				direction_horizontal = int((end_file - start_file) / abs(end_file - start_file))
				direction_vertical = int((end_rank - start_rank) / abs(end_rank - start_rank))
				for i in range(1, distance):
					assert not board[start_rank + i * direction_vertical][start_file + i * direction_horizontal], "cannot move there, a piece is in the way"
				return True
			elif (start_file == end_file and start_rank != end_rank) or (start_rank == end_rank and start_file != end_file): # move like a rook
				distance_horizontal = end_file - start_file
				direction_horizontal = 0 if distance_horizontal == 0 else int(distance_horizontal / abs(end_file - start_file))
				distance_vertical = end_rank - start_rank
				direction_vertical = 0 if distance_vertical == 0 else int(distance_vertical / abs(end_rank - start_rank))
				distance = max(abs(distance_horizontal), abs(distance_vertical))
				for i in range(1, distance):
					piece = board[start_rank + i * direction_vertical][start_file + i * direction_horizontal]
					assert not piece, "cannot move there, a piece is in the way"
				return True
			else:
				assert False, "queen can only move horizontally or diagonally"
			
			return True
		assert False, "unhandled exception"
	except AssertionError as e:
		error_msg = str(e)
		print(f"Error - {error_msg if error_msg else 'unknown exception'}")
		return False

		
			
def get_piece_char(piece: str, is_white: bool) -> str:
	if piece == 'P':
		return WHITE_PAWN if is_white else BLACK_PAWN
	elif piece == 'K':
		return WHITE_KING if is_white else BLACK_KING
	elif piece == 'N':
		return WHITE_KNIGHT if is_white else BLACK_KNIGHT
	elif piece == 'B':
		return WHITE_BISHOP if is_white else BLACK_BISHOP
	elif piece == 'R':
		return WHITE_ROOK if is_white else BLACK_ROOK
	elif piece == 'Q':
		return WHITE_QUEEN if is_white else BLACK_QUEEN
	return piece
			

if __name__ == "__main__":
    main()