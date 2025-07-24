#!/usr/bin/env python3
from enum import Enum
from ordered_set import OrderedSet

class Color(int, Enum):
    GREY   = (0, "#E0E0E0")
    GREEN  = (1, "#95c556")
    BLUE   = (2, "#7C97DF")
    YELLOW = (3, "#EBEBB4")
    BROWN  = (4, "#8E7878")
    RED    = (5, "#EE5252")
    ORANGE = (6, "#EDC16E")

    def __new__(cls, value, color):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.color = color
        return obj

# Community Game #158
board = [
    [Color.GREY, Color.GREEN, Color.BLUE, Color.YELLOW, Color.BROWN, Color.RED, Color.ORANGE],
    [Color.BLUE, Color.RED, Color.GREY, Color.ORANGE, Color.GREEN, Color.YELLOW, Color.BROWN],
    [Color.GREEN, Color.YELLOW, Color.BROWN, Color.GREY, Color.BLUE, Color.ORANGE, Color.GREY],
    [Color.BLUE, Color.ORANGE, Color.BLUE, Color.GREEN, Color.RED, Color.BROWN, Color.YELLOW],
    [Color.YELLOW, Color.BROWN, Color.RED, Color.GREY, Color.ORANGE, Color.BLUE, Color.GREEN],
    [Color.ORANGE, Color.BLUE, Color.GREEN, Color.BROWN, Color.RED, Color.GREY, Color.RED],
    [Color.BROWN, Color.GREY, Color.ORANGE, Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE]
]


# Pass in the board, and the available sets of columns, and colors
# The linkedin version of this game requires that no two queens are diagonally adjacent
# Diagonals more than one square apart are allowed
def solve(board):
    size = len(board)
    all_solutions = []

    def is_diagonally_adjacent(x, y, queens) -> bool:
        for qx, qy in queens:
            if abs(qx - x) == 1 and abs(qy - y) == 1:
                return True
        return False

    def solve_from(y, used_columns: set[int], used_colors: set[int], queens: set[tuple[int, int]]):
        if y == size:
            print_board(board, queens)
            all_solutions.append(queens.copy())
            return

        for x in range(size):
            color = board[y][x].value
            if x in used_columns or color in used_colors:
                continue
            if is_diagonally_adjacent(x, y, queens):
                continue

            solve_from(
                y + 1,
                used_columns | {x},
                used_colors | {color},
                queens | {(x, y)}
            )

    solve_from(0, set(), set(), set())
    return all_solutions


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def print_board(board, queens):
    RESET = "\033[0m"
    for y in range(len(board)):
        row = ""
        for x in range(len(board[y])):
            color_hex = board[y][x].color
            r, g, b = hex_to_rgb(color_hex)
            bg = f"\033[48;2;{r};{g};{b}m"
            cell = " 👑 " if (x, y) in queens else " \u3000 "  # full-width space
            row += f"{bg}{cell}{RESET}"
        print(row)
    print()


solutions = solve(board)