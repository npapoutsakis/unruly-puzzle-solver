#   AI Course - Prof. Lagoudakis - 2024
#           Nikolaos Papoutsakis
#               2019030206

# 1. Unruly game solver using Search Algorithms & Heuristics

def makeInitialBoard(file):
    with open(file, 'r') as f:
        line = f.readline().strip()

        # Decode line
        board_size, initial_state = line.split(":")
        rows, cols = map(int, board_size.split("x"))

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


def main():
    # Create board from file
    board = makeInitialBoard("board.txt")

    for row in board:
        print(' '.join(row))

    return


if __name__ == "__main__":
    main()
