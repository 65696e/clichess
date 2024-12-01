import re

EMPTY_BOARD = [["" for _ in range(8)] for _ in range(8)]

PIECES = ['k', 'n', 'b', 'p', 'r', 'q']

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

INTRO_MSG = """
███████████████████████████████████████████████████
█──▄▄▄█──████▄▄──▄▄█──▄▄▄█──██──█──▄▄▄█──▄▄▄█──▄▄▄█
█──████──██████──███──████──▄▄──█──▄▄██▄▄▄──█▄▄▄──█
█▄▄▄▄▄█▄▄▄▄▄█▄▄▄▄▄▄█▄▄▄▄▄█▄▄██▄▄█▄▄▄▄▄█▄▄▄▄▄█▄▄▄▄▄█

Welcome to clichess!

The command-line-interface for chess

How to play:

Each player will take turns typing in their move.
Your move should be written in chess notation.
If you don't know chess notation, you can learn it here:
https://www.chess.com/terms/chess-notation

You can also type your moves like this:

Pe2e4

The first character P is the first letter of the piece name (Pawn).
So to move your Queen, you would use Q.
Since King and Knight both start with K, use N for Knight.

The next two characters are the starting square, and the last two characters are the ending square.

So, 'Pe2e4' would move your Pawn from E2 to E4.

Type 'quit' at any time to quit.

Press Enter to start
"""



def main():
	print(INTRO_MSG)
	input(">> ")
	is_white: bool = True
	board: list[list[str]] = starting_board()
	draw(board)
	while True:
		turn = "White" if is_white else "Black"
		print(f"   {turn}'s turn. Please enter your move.\n")
		user_input: str = input(">> ").lower()
		if user_input == 'quit':
			print("\n   thanks for playing!")
			break
		processed_input = process_input(
			board=board,
			user_input=user_input,
			is_white=is_white,
		)
		if processed_input:
			(piece, start_file, start_rank, end_file, end_rank) = processed_input
			is_valid_move: bool = is_valid(
				board=board,
				is_white=is_white,
				piece=piece,
				start_file=start_file,
				start_rank=start_rank,
				end_file=end_file,
				end_rank=end_rank,
			)
			if is_valid_move:
				board[start_rank][start_file] = ''
				board[end_rank][end_file] = get_piece_char(piece, is_white=is_white)
				draw(board)
				is_white = not is_white
				continue
		else:
			print("   Invalid move")

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
			output += "  |█████     █████     █████     █████     |  \n"
		else:
			output += "  |     █████     █████     █████     █████|  \n"
		for x_idx, piece in enumerate(row):
			if x_idx == 0:
				output += f"{row_num} |"
			if is_light:
				if piece:
					output += f"█ {piece} █"
				else:
					output += "█████"
				
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
			output += f"  |█████{empty_space}█████{empty_space}█████{empty_space}█████{empty_space}|  \n"
		else:
			output += f"  |{empty_space}█████{empty_space}█████{empty_space}█████{empty_space}█████|  \n"
		is_light = not is_light
	output += "\n     a    b    c    d    e    f    g    h   \n"
	print(output)

def process_input(
	board: list[list[str]],
	user_input : str,
	is_white: bool,
) -> str | None:
	verbose_notation_regex = r"[pknqrb][a-h][1-8][a-h][1-8]"
	pawn_regex = r"[a-h][1-8]"
	pawn_capture_regex = r"[a-h][x][a-h][1-8]"
	piece_regex = r"[knqrb][a-h|1-8]?[x]?[a-h][1-8][+#]?"
	kingside_castle_notations = ["0-0", "o-o", "00", "oo", "castle king side", "castle kingside"]
	queenside_castle_notations = ["0-0-0", "o-o-o", "000", "ooo", "castle queen side", "castle queenside"]
	try:
		if re.fullmatch(verbose_notation_regex, user_input):
			piece = user_input[0]

			start_square = user_input[1:3]
			start_file = file_to_index(start_square[0])
			assert start_file >= 0 and start_file < 8
			start_rank = rank_to_index(start_square[1])
			assert start_rank >= 0 and start_rank < 8

			end_square = user_input[3:5]
			end_file = file_to_index(end_square[0])
			assert end_file >= 0 and start_file < 8
			end_rank = rank_to_index(end_square[1])
			assert end_rank >= 0 and end_rank < 8

			assert start_square != end_square
			return (piece, start_file, start_rank, end_file, end_rank)
		elif re.fullmatch(pawn_regex, user_input):
			piece = 'p'
			start_file = file_to_index(user_input[0])
			end_file = start_file
			end_rank = rank_to_index(user_input[1])
			pawn = WHITE_PAWN if is_white else BLACK_PAWN
			start_ranks = []
			for i in range(1,7):
				print(f"file={end_file}, rank={i}, piece={board[i][end_file]}")
				if board[i][end_file] == pawn:
					start_ranks.append(i)
			assert len(start_ranks) != 0, f"there are no pawns in that file"
			assert len(start_ranks) == 1, f"there are multiple pawns in that file. please specify which pawn you want to move (e.g. e4e5 means move the pawn on e4 to e5)"
			start_rank = start_ranks[0]
			return (piece, start_file, start_rank, end_file, end_rank)
		elif re.fullmatch(pawn_capture_regex, user_input):
			piece = 'p'
			start_file = file_to_index(user_input[0])
			end_file = file_to_index(user_input[2])
			end_rank = rank_to_index(user_input[3])
			pawn = WHITE_PAWN if is_white else BLACK_PAWN
			forward = -1 if is_white else 1
			start_rank = -1
			for i in range(1,7):
				print(f"file={start_file}, rank={i}, end_rank={end_rank} piece={board[i][end_file]}")
				if board[i][start_file] == pawn and i + forward == end_rank:
					start_rank = i
			assert start_rank >= 0, f"there are no pawns in that position"
			return (piece, start_file, start_rank, end_file, end_rank)
		elif re.fullmatch(piece_regex, user_input):
			#print(f"piece={piece}, start_rank={start_rank},start_file={start_file} end_rank={end_rank},end_file={end_file}")

			piece_regex = r"[knqrb][a-h|1-8]?[x]?[a-h][1-8][+#]?"
			piece = user_input[0]
			piece_char = get_piece_char(piece, is_white)
			offset = 0
			# TODO: add logic to differentiate between ambiguous moves (e.g. Nfxc3, R3e4)
			if user_input[offset+1] == 'x':
				offset += 1
			end_file = file_to_index(user_input[offset+1])
			end_rank = rank_to_index(user_input[offset+2])
			start_file = -1
			start_rank = -1
			for y, row in enumerate(board):
				for x, square in enumerate(row):
					if square == piece_char:
						if is_valid(board, is_white, piece, x, y, end_file, end_rank, log_error=False):
							start_file = x
							start_rank = y
							break
			if start_file >= 0 and start_rank >= 0:
				return (piece, start_file, start_rank, end_file, end_rank)
			else:
				return None
			# todo - pieces
			return None
		elif user_input in kingside_castle_notations:
			# todo castling
			return None
		elif user_input in queenside_castle_notations:
			# todo castling
			return None
		else:
			return None
	except AssertionError as e:
		error_msg = str(e)
		print(f"   Error - {error_msg if error_msg else 'unknown assertion exception'}")
		return None
	except IndexError as e:
		error_msg = str(e)
		print(f"   Error - {error_msg if error_msg else 'unknown index exception'}")
		return None


def is_valid(
	board: list[list[str]],
	is_white: bool,
	piece: str,
	start_file: int,
	start_rank: int,
	end_file: int,
	end_rank: int,
	log_error: bool = True
) -> bool:
	try:
		#print(f"piece={piece}, start_rank={start_rank},start_file={start_file} end_rank={end_rank},end_file={end_file}")
		friendly_pieces = WHITE_PIECES if is_white else BLACK_PIECES
		start_piece = board[start_rank][start_file]
		assert start_piece, "there is not a piece at your starting square"
		assert start_piece in friendly_pieces, "the piece at your starting square does not belong to you"
		end_piece = board[end_rank][end_file]
		assert end_piece not in friendly_pieces, "cannot move there, one of your pieces is in the way"
		is_end_empty = not end_piece
		if piece == 'p':
			forward = -1 if is_white else 1
			is_first_move = start_rank == (6 if is_white else 1)
			if is_end_empty:
				assert start_file == end_file, "pawns must move vertically, unless capturing"
				if end_rank == start_rank + forward:
					return True
				elif end_rank == start_rank + 2 * forward and is_first_move:
					is_path_empty = not board[start_rank + forward][end_file]
					assert is_path_empty, "the pawn's path is blocked"
					return True
				else:
					assert False, "pawns can only move forward"
			else:
				assert (end_file == start_file + 1 or end_file == start_file - 1), "pawns can only capture diagonally"
				assert (end_rank == start_rank + forward), "pawns can only move forward"
				return True
		elif piece == 'k':
			assert abs(start_file - end_file) <= 1 and abs(start_rank - end_rank) <= 1, "king can only move one square in any direction"
			return True
		elif piece == 'n':
			assert abs(start_file - end_file) <= 2 and abs(start_rank - end_rank) <= 2, "knights cannot move that far"
			assert abs(start_file - end_file) + abs(start_rank - end_rank) == 3, "knights must move in an L shape"
			return True
		elif piece == 'b':
			assert abs(start_file - end_file) == abs(start_rank - end_rank), "bishops can only move diagonally"
			distance = abs(start_file - end_file)
			direction_horizontal = int((end_file - start_file) / abs(end_file - start_file))
			direction_vertical = int((end_rank - start_rank) / abs(end_rank - start_rank))
			for i in range(1, distance):
				assert not board[start_rank + i * direction_vertical][start_file + i * direction_horizontal], "cannot move there, a piece is in the way"
			return True
		elif piece == 'r':
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
		elif piece == 'q':
			# move like a bishop
			if abs(start_file - end_file) == abs(start_rank - end_rank):
				distance = abs(start_file - end_file)
				direction_horizontal = int((end_file - start_file) / abs(end_file - start_file))
				direction_vertical = int((end_rank - start_rank) / abs(end_rank - start_rank))
				for i in range(1, distance):
					assert not board[start_rank + i * direction_vertical][start_file + i * direction_horizontal], "cannot move there, a piece is in the way"
				return True
			# move like a rook
			elif (start_file == end_file and start_rank != end_rank) or (start_rank == end_rank and start_file != end_file):
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
		assert False, "unhandled exception"
	except AssertionError as e:
		error_msg = str(e)
		if log_error:
			print(f"   Error - {error_msg if error_msg else 'unknown assertion exception'}")
		return False
	except IndexError as e:
		error_msg = str(e)
		if log_error:
			print(f"   Error - {error_msg if error_msg else 'unknown index exception'}")
		return False

		
			
def get_piece_char(piece: str, is_white: bool) -> str:
	if piece == 'p':
		return WHITE_PAWN if is_white else BLACK_PAWN
	elif piece == 'k':
		return WHITE_KING if is_white else BLACK_KING
	elif piece == 'n':
		return WHITE_KNIGHT if is_white else BLACK_KNIGHT
	elif piece == 'b':
		return WHITE_BISHOP if is_white else BLACK_BISHOP
	elif piece == 'r':
		return WHITE_ROOK if is_white else BLACK_ROOK
	elif piece == 'q':
		return WHITE_QUEEN if is_white else BLACK_QUEEN
	return piece

# converts the file to the corresponding index in a 2d array
# e.g. 'a' -> 0
def file_to_index(file: str) -> int:
	return ord(file) - ord('a')

# converts the rank to the corresponding index in a 2d array
# e.g. '1' -> 7
# remember the top of the board corresponds to the bottom of the array, so rank 1 is the 7th row in the array
def rank_to_index(rank: str) -> int:
	return 7 - (int(rank) - 1)

if __name__ == "__main__":
    main()