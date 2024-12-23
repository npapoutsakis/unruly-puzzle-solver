#   AI Course - Prof. Lagoudakis - 2024
#           Nikolaos Papoutsakis
#               2019030206

# 1. Unruly game solver using Search Algorithms & Heuristics

def makeInitialBoard(file):
    with open(file, 'r') as f:
        line = f.readline().strip()

        # Decode line
        board_size, initial_state = line.split(":")
        
        rows = int(board_size[0])
        cols = int(board_size[2])

        # Initialize the board
        board = [["." for _ in range(cols)] for _ in range(rows)]

    # Track current position
    current_position = 0

    for char in initial_state:
        # Calculate number of steps from character
        steps = ord(char.lower()) - ord('a') + 1
        current_position += steps

        # Place a tile if within board limits
        if current_position <= rows * cols:
            row = (current_position - 1) // cols
            col = (current_position - 1) % cols

            # 'W' for lowercase, 'B' for uppercase
            board[row][col] = 'W' if char.islower() else 'B'

    return board


def printBoard(board):
    for row in board:
        print(' '.join(row))
    return

def is_valid(board, row, col, color):
    n = len(board)
    
    # Copy the board and try placing the color
    board[row][col] = color
    
    # Check row constraints
    row_str = ''.join(board[row])
    col_str = ''.join([board[r][col] for r in range(n)])
    
    if 'BBB' in row_str or 'WWW' in row_str:
        board[row][col] = '.'
        return False
    if 'BBB' in col_str or 'WWW' in col_str:
        board[row][col] = '.'
        return False
    
    # Count number of 'B' and 'W' in row/column
    if row_str.count('B') > n // 2 or row_str.count('W') > n // 2:
        board[row][col] = '.'
        return False
    if col_str.count('B') > n // 2 or col_str.count('W') > n // 2:
        board[row][col] = '.'
        return False
    
    board[row][col] = '.'
    return True


def backtrack(board, row, col):
    n = len(board)
    # If we reached the end of the board
    if row == n:
        return True

    # Move to the next cell
    next_row = row + 1 if col == n - 1 else row
    next_col = (col + 1) % n

    # Skip already filled cells
    if board[row][col] != '.':
        return backtrack(board, next_row, next_col)

    # Try placing 'B' and 'W'
    for color in ['B', 'W']:
        if is_valid(board, row, col, color):
            board[row][col] = color
            if backtrack(board, next_row, next_col):
                return True
            board[row][col] = '.'  # Undo and backtrack

    return False


def solve(board):

    if backtrack(board, 0, 0):
        print("Solution Found:")
        printBoard(board)
    else:
        print("No Solution Found")



def main():
    # create board from file
    board = makeInitialBoard("board.txt")

    solve(board)

    return


if __name__ == "__main__":
    main()
