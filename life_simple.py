"""
Author: Leo Vidarte <http://nerdlabs.com.ar>

This is free software,
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.

"""

"""
Las transiciones dependen del número de células vecinas vivas:

  * Una célula muerta con exactamente 3 células vecinas vivas "nace"
    (al turno siguiente estará viva).
  * Una célula viva con 2 ó 3 células vecinas vivas sigue viva,
    en otro caso muere o permanece muerta (por "soledad" o "superpoblación").

"""

# Glider
board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

WIDTH = len(board[0])
HEIGHT = len(board)

def get_neighbors(cell, board):
    x_center, y_center = cell

    x_left  = x_center-1 if x_center-1 >= 0 else WIDTH-1
    x_right = x_center+1 if x_center+1 < WIDTH else 0
    y_up    = y_center-1 if y_center-1 >= 0 else HEIGHT-1
    y_down  = y_center+1 if y_center+1 < HEIGHT else 0

    return (board[y_up][x_left],
            board[y_up][x_center],
            board[y_up][x_right],
            board[y_center][x_left],
            board[y_center][x_right],
            board[y_down][x_left],
            board[y_down][x_center],
            board[y_down][x_right],)

def evolve(board):
    board_ = [[0] * WIDTH for _ in range(HEIGHT)]
    for x in range(WIDTH):
        for y in range(HEIGHT):
            v = board[y][x]
            n = get_neighbors((x, y), board)
            t = n.count(1)
            # Born or survive
            if (v == 0 and t == 3) or \
               (v == 1 and t in (2, 3)):
                board_[y][x] = 1
    return board_

def show(board):
    for row in board:
        for col in row:
            cell = ' ' if col == 0 else '#'
            print(cell, end='')
        print()

for i in range(30):
    show(board)
    board = evolve(board)
    print("-" * 16)

