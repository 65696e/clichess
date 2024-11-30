EMPTY_BOARD = [["" for _ in range(8)] for _ in range(8)]

WHITE_KING = '♚'
WHITE_QUEEN = '♛'
WHITE_BISHOP = '♝'
WHITE_KNIGHT = '♞'
WHITE_ROOK = '♜'
WHITE_PAWN = '♟'

BLACK_KING = '♔'
BLACK_QUEEN = '♕'
BLACK_BISHOP = '♗'
BLACK_KNIGHT = '♘'
BLACK_ROOK = '♖'
BLACK_PAWN = '♙'



def main():
	print("welcome to clichess")
	input("press enter to start")
	board = starting_board()
	while True:
		print(draw(board))
		user_input = input(">> ")
		if user_input.lower() == 'quit':
			print("bye!")
			break
		print(f"you typed: {user_input}")

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
	board[0][3] = BLACK_KING
	board[7][4] = WHITE_KING
	# queens
	board[0][4] = BLACK_QUEEN
	board[7][3] = WHITE_QUEEN
	return board

def draw(
	board,
):
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
	return output
			

if __name__ == "__main__":
    main()