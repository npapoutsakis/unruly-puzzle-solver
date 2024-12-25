# Unruly Game Solver

### AI Course - Prof. Lagoudakis - 2024

**Author:** Nikolaos Papoutsakis**Student ID:** 2019030206

## Project Description

This project is a Python-based solver for the Unruly logic game using a **Backtracking Algorithm**. The solver fills the empty spaces of an initial board to satisfy the following conditions:

1. Each row and column must contain an equal number of black (`B`) and white (`W`) squares.
2. No three consecutive squares in any row or column can have the same color.

The algorithm uses **backtracking** to try different combinations of black and white squares to find a valid solution.

---

## How to Run the Solver

1. Place the initial board configuration in a text file (e.g., `board.txt`).
2. Run the Python script by executing the following command:
   ```bash
   python unruly_solver.py
   ```
3. Enter the maximum number of nodes to expand during the search when prompted.
4. The solution (if found) will be printed to the console and saved to `output.txt`.

---

## Input File Format

The input file should follow this format:

```
8x8:bceadEDgCcAgCcabBi
```

- `8x8` specifies the board dimensions (rows x columns).
- `bceadEDgCcAgCcabBi` encodes the initial state, where:
  - Lowercase letters (`a-z`) represent white (`W`) squares.
  - Uppercase letters (`A-Z`) represent black (`B`) squares.
  - The letters indicate the position by stepping forward a certain number of squares, starting from the top-left corner.

---

## Output

- If the solver finds a solution, the completed board is saved in `output.txt` in the same encoding format as the input.
- If no solution is found, the program will notify the user.

---

## Example

### Input (board.txt):

```
8x8:bceadEDgCcAgCcabBi
```

### Console Output:

```
Initial Board:
. W . . W . . .
. W W . . . W .
. . . B . . . B
. . . . . . W .
. B . . W B . .
. . . . W . . B
. . W W . W . B
. . . . . . . .

Solution Found:
B W B W W B B W
B W W B B W W B
W B W B W W B B
B W B W B B W W
W B W B W B B W
W W B B W W B B
B B W W B W W B
W B B W B B W W

Execution time: 0.002 seconds
Nodes expanded: 161
```

---

## Requirements

- Python 3.x

---

## Notes

- The backtracking algorithm may take longer for larger board sizes. Limiting the number of node expansions can help avoid long computation times.
- The project is designed to handle boards of size 6x6 or larger (even dimensions only).

---

**Enjoy solving Unruly puzzles with AI!**
