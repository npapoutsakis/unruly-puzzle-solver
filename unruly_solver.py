#   AI Course - Prof. Lagoudakis - 2024
#           Nikolaos Papoutsakis
#               2019030206

# 4. Unruly game solver (csp) using Backtracking Search Algorithm
import time

# Print the board
def printBoard(board):
    for row in board:
        print(' '.join(row))
    
    print()
    return
        
# Reading input file & decode the initial board
def makeInitialBoard(file):
    with open(file, 'r') as f:
        line = f.readline().strip()

        # Decode line
        board_size = line.split(":")[0]
        initial_state = line.split(":")[1]
        
        # get the rows and cols of each board
        rows, cols = map(int, board_size.split('x'))

        if rows < 6 or cols < 6 or rows % 2 != 0 or cols % 2 != 0:
            exit("ERROR: n>=6, m>=6 and n,m even numbers")
        
        # fill the board with the initial state given in the file
        board = []
        for _ in range(rows):
            row = []
            for _ in range(cols):
                row.append(".")
            board.append(row)


    current_position = 0
    for char in initial_state:
        # Calculate number of steps from character
        # ord() returns the ASCII value of a character
        steps = ord(char.lower()) - ord('a') + 1

        # each step is a box on the board, just add the steps i ve done
        current_position += steps

        # check limits - 8x8 = 64.
        if current_position <= rows * cols:
            # Calculate row and column of current position
            # start from current_position - 1
            row = (current_position - 1) // cols
            col = (current_position - 1) % cols

            # 'W' for lowercase, 'B' for uppercase
            if char.islower():
                board[row][col] = 'W'
            else:
                board[row][col] = 'B'

    return board

# Check if the board is correctly filled
def is_ok(board):
    for row in board:
        # check each 
        if not correct(row):
            return False
    
    cols = len(board[0])
    rows = len(board)
    
    for c in range(cols):
        col = [board[r][c] for r in range(rows)]
        if not correct(col):
            return False
    
    return True

# Check if a line is correct
def correct(line):
    # count blacks and whites to see the balance
    if line.count('B') > len(line) // 2 or line.count('W') > len(line) // 2:
        return False
    
    # for each place in the line(row or col), check if there are 3 consecutive colors
    for i in range(len(line) - 2):
        if line[i] == line[i + 1] == line[i + 2] and line[i] != '.':
            return False
    
    return True

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

    # write to file
    with open("output.txt", "w") as file:
        file.write(output)
    
    return

# https://www.geeksforgeeks.org/backtracking-algorithm-in-python/
# Backtracking Algorithm
def backtracking_search(board, row, col, expanded_nodes, max_expansions):
    # at first stop and return false if the expanded nodes are greater the limit given
    if expanded_nodes >= max_expansions:
        return False, expanded_nodes
    
    # increase the nodes on each call
    expanded_nodes += 1
    
    # If we reach the end of the board, the solution is found
    if row == len(board):
        return True, expanded_nodes
    
    # get the next row and col
    next_row = row + (col + 1) // len(board[0])
    next_col = (col + 1) % len(board[0])

    # skiping and call if a letter is already there
    if board[row][col] != '.':
        return backtracking_search(board, next_row, next_col, expanded_nodes, max_expansions)

    for placement in 'BW':
        # place the color to that position
        board[row][col] = placement
        
        # if its validn then call again to the next position
        if is_ok(board):
            result, expanded_nodes = backtracking_search(board, next_row, next_col, expanded_nodes, max_expansions)
            if result:
                return True, expanded_nodes
        # else just leave it empty
        board[row][col] = '.'

    return False, expanded_nodes


# main()
def main():
    input_file = input("Give me the input file: ")
    node_expansion = int(input("Max nodes to expand: "))

    board = makeInitialBoard(input_file)
    
    print("Initial Board:")
    printBoard(board)
    
    start_time = time.time()
    solution, total_nodes = backtracking_search(board, 0, 0, 0, node_expansion)

    if solution:
        print("Solution Found:")
        printBoard(board)
        encodeSolution(board)
    else:
        print("No solution found.")

    print(f"Execution time: {time.time() - start_time:.3f} seconds")
    print(f"Nodes expanded: {total_nodes}")

    return


if __name__ == "__main__":
    main()
