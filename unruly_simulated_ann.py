#   AI Course - Prof. Lagoudakis - 2024
#           Nikolaos Papoutsakis
#               2019030206

# 5. Unruly game using Simulated Annealing Algorithm

import time
import random
import numpy as np
import sys

# Print the board
def printBoard(board):
    for row in board:
        print(' '.join(row))
    
    print()
    return

# Return true with probability p.
def probability(p):
    return p > random.uniform(0.0, 1.0)


# Map the time to a temperature
def exp_schedule(k=20, limit=100):
    lam = -np.log(k) / limit
    return lambda t: (k * np.exp(-lam * t) if t < limit else 0)


# This is the evaluation function f(s)
def evaluate(current_state):
    f_s = 0 # or np.inf ?

    # Row and column checks
    for i in range(len(current_state)):
        row_counting = {'B': 0, 'W': 0}
        triples = 0
        for j in range(len(current_state[0])):
            row_counting[current_state[i][j]] += 1
            if j >= 2 and current_state[i][j] == current_state[i][j-1] == current_state[i][j-2]:
                triples += 1
        f_s += abs(row_counting['B'] - row_counting['W']) + triples

    for j in range(len(current_state[0])):
        column_counting = {'B': 0, 'W': 0}
        triples = 0
        for i in range(len(current_state)):
            column_counting[current_state[i][j]] += 1
            if i >= 2 and current_state[i][j] == current_state[i-1][j] == current_state[i-2][j]:
                triples += 1
        f_s += abs(column_counting['B'] - column_counting['W']) + triples

    # returns the f(current_state)
    return f_s


# Fill the board randomly
def fill_randomly(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '.':
                board[i][j] = random.choice(['B', 'W'])
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
    # to save the initial state of the board
    pre_colored = [[False for _ in range(rows)] for _ in range(cols)]
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
                pre_colored[row][col] = True
            else:
                board[row][col] = 'B'
                pre_colored[row][col] = True

    return board, pre_colored

# get the neighbors of the current state
def get_neighbors(board, pre_colored):
    n = len(board)
    m = len(board[0])
    neighbors = []
    
    for _ in range(5): 
        new_grid = [row[:] for row in board]

        # choose a random neigbor
        i, j = random.randint(0, n-1), random.randint(0, m-1)
        
        if not pre_colored[i][j]:
            if board[i][j] == 'B':
                new_grid[i][j] = 'W'
            else:
                new_grid[i][j] = 'B'

            neighbors.append(new_grid)
    
    return neighbors

# Simulated Annealing Algorithm
def simulated_annealing(board, pre_colored, schedule=exp_schedule()):
    current_state = board
    best_state = board
    best_f_s = evaluate(board)


    for t in range(sys.maxsize):
        T = schedule(t)
        if T == 0:
            break

        neighbors = get_neighbors(current_state, pre_colored)
        if not neighbors:
            break
        
        next_state = random.choice(neighbors)
        delta_e = evaluate(current_state) - evaluate(next_state)

        # Accept the new state with probability based on temperature
        if delta_e > 0 or probability(np.exp(delta_e / T)):
            current_state = next_state
            if evaluate(current_state) < best_f_s:
                best_state = current_state
                best_f_s = evaluate(current_state)
    
    return best_state, best_f_s, t



# Main
def main():
    random.seed(time.time())
    input_file = input("Give me the input file: ")
    local_moves = int(input("Maximum number of steps: "))

    board, pre_colored = makeInitialBoard(input_file)

    # used to add violations to the board
    fill_randomly(board)

    print("Initial board:")
    printBoard(board)

    start_time = time.time()

    # adjust the scheduling function to the steps given
    solution, violations, steps = simulated_annealing(board, pre_colored, schedule=exp_schedule(limit=local_moves))
    
    if solution:
        print("Final board:")
        printBoard(board)
    else:
        print("No solution found.")

    print(f"Execution time: {time.time() - start_time:.3f} seconds")
    print(f"Steps done: {steps}")
    print(f"Violations: {violations}")
    
    return



if __name__ == "__main__":
    main()

