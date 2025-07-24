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

# Community Game 
board = [
    [Color.GREY, Color.GREEN, Color.BLUE, Color.YELLOW, Color.BROWN, Color.RED, Color.ORANGE],
    [Color.BLUE, Color.RED, Color.GREY, Color.ORANGE, Color.GREEN, Color.YELLOW, Color.BROWN],
    [Color.GREEN, Color.YELLOW, Color.BROWN, Color.GREY, Color.BLUE, Color.ORANGE, Color.GREY],
    [Color.BLUE, Color.ORANGE, Color.BLUE, Color.GREEN, Color.RED, Color.BROWN, Color.YELLOW],
    [Color.YELLOW, Color.BROWN, Color.RED, Color.GREY, Color.ORANGE, Color.BLUE, Color.GREEN],
    [Color.ORANGE, Color.BLUE, Color.GREEN, Color.BROWN, Color.RED, Color.GREY, Color.RED],
    [Color.BROWN, Color.GREY, Color.ORANGE, Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE]
]


# Pass in the board, and the available sets of rows, columns, and colors
def solve(board, column_sets, color_sets) -> set:

    def place_queen(x, y):
        queens.add((x, y))
        column_sets.remove(x)
        color_sets.remove(board[y][x].value)

    def remove_queen(x, y):
        queens.remove((x, y))
        column_sets.add(x)
        color_sets.add(board[y][x].value)

    # The linkedin version of this game requires that no two queens are diagonally adjacent
    # Diagonals more than one square apart are allowed
    def is_diagonally_adjacent(x, y, queens) -> bool:
        for qx, qy in queens:
            if abs(qx - x) == 1 and abs(qy - y) == 1:
                return True
        return False

    def solve_from(board, y, column_sets, color_sets, queens):
        if len(queens) == vsize:
            print_board(board, queens) # Print the board when a solution is found
            return queens

        for x in list(column_sets):
            color = board[y][x].value
            if color in color_sets and not is_diagonally_adjacent(x, y, queens):
                place_queen(x, y)
                solve_from(board, y+1, column_sets, color_sets, queens)
                # Keep looking for more solutions
                remove_queen(x, y)
        return set() # no solution found

    queens = set()
    for x in list(column_sets):
        place_queen(x, 0) # Can always place a queen in the first row
        solve_from(board, 1, column_sets, color_sets, queens)
        remove_queen(x, 0)


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


vsize = len(board)
assert all(vsize == len(row) for row in board)

# create row, column and color sets of available positions
column_sets = OrderedSet(range(vsize))
color_sets = OrderedSet(range(len(Color)))

queens = solve(board, column_sets, color_sets)