#   AI Course - Prof. Lagoudakis - 2024
#           Nikolaos Papoutsakis
#               2019030206

# 1. Unruly game solver using A* Search Algorithm & Heuristic

import heapq
import time

# Check if the board is valid after placing a color at a specific position
def is_valid(board, row, col, color):
    n = len(board)
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

def heuristic(board):
    imbalance = 0
    triplets = 0
    empty_cells = 0

    for row in board:
        imbalance += abs(row.count('B') - row.count('W'))  # Difference between B and W
        empty_cells += row.count('.')  # Count empty cells in the row

        # Count triplets directly in the loop without a helper function
        for i in range(len(row) - 2):
            if row[i] == row[i+1] and row[i+1] != '.' and row[i+2] == '.':
                triplets += 1

    # Check each column for imbalance, triplets, and empty cells (without zip)
    n = len(board)
    for col in range(n):
        col_values = [board[row][col] for row in range(n)]  # Extract column manually
        imbalance += abs(col_values.count('B') - col_values.count('W'))
        
        for i in range(len(col_values) - 2):
            if col_values[i] == col_values[i+1] and col_values[i+1] != '.' and col_values[i+2] == '.':
                triplets += 1

    # Return total imbalance, triplets, and empty cells as heuristic value
    return imbalance + triplets + empty_cells


# https://www.geeksforgeeks.org/a-search-algorithm/
# A* Search Algorithm
def a_star(board, max_nodes, cutoff=100):
    n = len(board)
    open_list = []
    heapq.heappush(open_list, (0, board, 0))  # (f, board, g)
    nodes_expanded = 0

    while open_list and nodes_expanded < max_nodes:
        f, current_board, g = heapq.heappop(open_list)
        nodes_expanded += 1

        print(f"Nodes Expanded: {nodes_expanded}")
        printBoard(current_board)
        # Check if the solution is complete
        if isSolution(current_board):
            print("SOLVED!")
            print(f"Nodes Expanded: {nodes_expanded}")
            return current_board
        
        # Stop expanding if cutoff is reached
        if f > cutoff:
            continue

        # Expand neighbors for empty cells
        for row in range(n):
            for col in range(n):
                if current_board[row][col] == '.':
                    for color in ['B', 'W']:
                        new_board = [r[:] for r in current_board]
                        if is_valid(new_board, row, col, color):
                            new_board[row][col] = color
                            f_new = g + heuristic(new_board)
                            
                            # Prune branches exceeding cutoff
                            if f_new < cutoff:
                                heapq.heappush(open_list, (f_new, new_board, g + 1))
 
                    break

    print("Max node expansion limit reached.")
    return None

# Check if the board has a correct solution
def isSolution(board):
    # Check each row to see if it has the correct number of 'B' and 'W'
    for row in range(len(board)):
        blacks = board[row].count('B')
        whites = board[row].count('W')
        
        if blacks != len(board) / 2 or whites != len(board) / 2:
            return False
    return True

def printBoard(board):
    for row in board:
        print(' '.join(row))
    return

# Reading input file & decode the initial board
def makeInitialBoard(file):
    with open(file, 'r') as f:
        line = f.readline().strip()

        # Decode line
        board_size, initial_state = line.split(":")
        
        rows, cols = map(int, board_size.split('x'))

        board = [["." for _ in range(cols)] for _ in range(rows)]

    current_position = 0

    for char in initial_state:
        # Calculate number of steps from character
        # ord() returns the ASCII value of a character
        steps = ord(char.lower()) - ord('a') + 1

        # Update current position on board by steps taken from character value
        current_position += steps

        # Place a tile if within board limits - 8x8 = 64.
        if current_position <= rows * cols:
            # Calculate row and column of current position
            row = (current_position - 1) // cols
            col = (current_position - 1) % cols

            # 'W' for lowercase, 'B' for uppercase
            if char.islower():
                board[row][col] = 'W'
            else:
                board[row][col] = 'B'

    return board

# encode the solution
def encodeSolution(solution):
        
    # get the dimensions of the board
    rows = len(solution)
    cols = len(solution[0])

    encoded_solution = ""
    for row in solution:
        for char in row:
            if char == 'W':
                encoded_solution += 'a'
            else:
                encoded_solution += 'A'
    
    encoded_solution += '\n'

    # create output string
    output = f"{rows}x{cols}:{encoded_solution}"

    with open("output.txt", "w") as file:
        file.write(output)
    
    return

# Main
def main():
    input_file = "board.txt"
    # input_file = input("Enter the input file name: ")
    max_nodes = int(input("Enter the maximum number of nodes to expand: "))
    
    board = makeInitialBoard(input_file)
    printBoard(board)

    start_time = time.time()
    solution = a_star(board, max_nodes)
    end_time = time.time()

    if solution is not None:
        print(f"Time Taken: {end_time - start_time} seconds")
        encodeSolution(solution)
    else:
        print("No Solution Found")



if __name__ == "__main__":
    main()