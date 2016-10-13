#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Leo Vidarte <http://nerdlabs.com.ar>

This is free software,
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.

"""

import Tkinter as tk


class Application(tk.Frame):

    def __init__(self, width, height, size=10):
        tk.Frame.__init__(self)
        self.grid()
        self.width = width
        self.height = height
        self.size = size
        self.board = [[0] * width for _ in xrange(height)]
        self.create_widgets()
        self.draw_grid()
        self.create_events()

    def create_widgets(self):
        width = self.width * self.size
        height = self.height * self.size
        self.canvas = tk.Canvas(self, width=width, height=height, bg='white')
        self.canvas.grid()
        self.status = tk.Label(self, text="click on board to add or remove cells")
        self.status.grid()

    def draw_grid(self):
        color = 'gray'
        for i in xrange(self.width - 1):
            x = (self.size * i) + self.size
            y0 = 0
            y1 = self.size * self.height
            self.canvas.create_line(x, y0, x, y1, fill=color)
        for i in xrange(self.height - 1):
            x0 = 0
            x1 = self.size * self.width
            y = (self.size * i) + self.size
            self.canvas.create_line(x0, y, x1, y, fill=color)

    def create_events(self):
        self.canvas.bind_all('<Button-1>', self.toggle_cell)

    def toggle_cell(self, event):
        x = event.x / self.size
        y = event.y / self.size
        if self.board[y][x] == 0:
            x0 = x * self.size
            y0 = y * self.size
            x1 = x0 + self.size
            y1 = y0 + self.size
            id = self.canvas.create_rectangle(x0, y0, x1, y1,
                                              width=0, fill='black')
            self.board[y][x] = id
        else:
            self.canvas.delete(self.board[y][x])
            self.board[y][x] = 0


if __name__ == '__main__':

    from optparse import OptionParser
    parser = OptionParser(description="Random maze game")
    parser.add_option('-W', '--width', type=int, default=20,
                      help="maze width (must be odd)")
    parser.add_option('-H', '--height', type=int, default=20,
                      help="maze height (must be odd)")
    parser.add_option('-s', '--size', type=int, default=15,
                      help="cell size")
    args, _ = parser.parse_args()

    app = Application(args.width, args.height, args.size)
    app.master.title('Game of life')
    app.mainloop()

