#!/usr/bin/env python3
"""
3x3 Sliding Tile Puzzle (8-puzzle) for the terminal.

Controls:
- W: move blank up
- A: move blank left
- S: move blank down
- D: move blank right
- Q: quit
"""

from __future__ import annotations

import random
import time
from typing import List, Tuple

Board = List[List[int]]

GOAL_STATE: Board = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0],  # 0 represents the blank tile
]


def flatten(board: Board) -> List[int]:
    """Convert a 2D board into a flat list."""
    return [tile for row in board for tile in row]


def inversion_count(flat_tiles: List[int]) -> int:
    """Count inversions (ignoring the blank/0)."""
    numbers = [n for n in flat_tiles if n != 0]
    inversions = 0
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] > numbers[j]:
                inversions += 1
    return inversions


def is_solvable(board: Board) -> bool:
    """Check solvability for a 3x3 puzzle.

    For odd grid width (3), a state is solvable if inversion count is even.
    """
    inv = inversion_count(flatten(board))
    return inv % 2 == 0


def make_random_solvable_board() -> Board:
    """Generate a random solvable board that is not already solved."""
    tiles = list(range(9))
    while True:
        random.shuffle(tiles)
        board = [tiles[i : i + 3] for i in range(0, 9, 3)]
        if board != GOAL_STATE and is_solvable(board):
            return board


def find_blank(board: Board) -> Tuple[int, int]:
    """Return (row, col) of blank tile (0)."""
    for r, row in enumerate(board):
        for c, value in enumerate(row):
            if value == 0:
                return r, c
    raise ValueError("Board has no blank tile.")


def try_move(board: Board, direction: str) -> bool:
    """Try to move the blank in a given direction.

    Returns True if move succeeded, False if the move is invalid.
    """
    r, c = find_blank(board)

    # Direction maps to row/col delta for blank movement.
    deltas = {
        "w": (-1, 0),
        "a": (0, -1),
        "s": (1, 0),
        "d": (0, 1),
    }

    if direction not in deltas:
        return False

    dr, dc = deltas[direction]
    nr, nc = r + dr, c + dc

    # Reject moves that go out of bounds.
    if not (0 <= nr < 3 and 0 <= nc < 3):
        return False

    # Swap blank with adjacent tile.
    board[r][c], board[nr][nc] = board[nr][nc], board[r][c]
    return True


def is_win(board: Board) -> bool:
    """Return True when board matches the goal state."""
    return board == GOAL_STATE


def draw_board(board: Board) -> None:
    """Print the board in a readable text format."""
    print("\n+---+---+---+")
    for row in board:
        rendered = [" " if n == 0 else str(n) for n in row]
        print(f"| {rendered[0]:>1} | {rendered[1]:>1} | {rendered[2]:>1} |")
        print("+---+---+---+")


def main() -> None:
    """Run the sliding puzzle game loop."""
    board = make_random_solvable_board()
    moves = 0
    start_time = time.monotonic()

    print("Welcome to the 3x3 Sliding Tile Puzzle!")
    print("Use W/A/S/D to move the blank tile. Press Q to quit.")

    while True:
        draw_board(board)

        if is_win(board):
            elapsed_seconds = time.monotonic() - start_time
            print(f"Congratulations! You solved the puzzle in {moves} moves.")
            print(f"Elapsed time: {elapsed_seconds:.2f} seconds.")
            break

        command = input("Move (W/A/S/D, Q to quit): ").strip().lower()
        if not command:
            print("Please enter a key.")
            continue

        key = command[0]
        if key == "q":
            print("Goodbye!")
            break

        moved = try_move(board, key)
        if moved:
            moves += 1
            print(f"Move count: {moves}")
        else:
            print("Invalid move. Try W/A/S/D.")


if __name__ == "__main__":
    main()
