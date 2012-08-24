#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import Tkinter as tk


class Application(tk.Frame):

    def __init__(self, width, height, size=10):
        tk.Frame.__init__(self)
        self.width = width
        self.height = height
        self.size = size
        self.grid()
        self.create_widgets()
        self.init_life()
        self.draw_grid()
        self.create_events()

    def init_life(self):
        self.life = Life(self.width, self.height)
        if getattr(self, 'living_cells', None) is None:
            self.living_cells = {}
        self.clear_screen()
        self._speeds = [i/10.0 for i in range(1, 11)][::-1]
        self._running = False
        self.scl_steps.set(1)
        self.scl_speed.set(10)

    def clear_screen(self):
        for id in self.living_cells.values():
            self.canvas.delete(id)
        self.living_cells = {}

    def create_widgets(self):
        width = self.width * self.size
        height = self.height * self.size
        self.canvas = tk.Canvas(self, width=width, height=height, bg='white')
        self.canvas.grid(row=0, column=0)

        self.status = tk.Label(self, text="click to add or remove cells")
        self.status.grid(row=1, column=0)

        self.sidebar = tk.Frame()
        self.sidebar.grid(row=0, column=1, rowspan=2, sticky=tk.N)

        self.scl_steps = tk.Scale(self.sidebar, from_=1, to=100,
                                  label='steps', orient=tk.HORIZONTAL)
        self.scl_steps.grid()

        self.scl_speed = tk.Scale(self.sidebar, from_=1, to=10,
                                  label='speed', orient=tk.HORIZONTAL)
        self.scl_speed.grid()
 
        self.btn_start = tk.Button(self.sidebar, text="Start",
                                   command=self.start)
        self.btn_start.grid()

        self.btn_stop = tk.Button(self.sidebar, text="Stop",
                                  command=self.stop)
        self.btn_stop.grid()

        self.btn_reset = tk.Button(self.sidebar, text="Reset",
                                  command=self.init_life)
        self.btn_reset.grid()


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
        if isinstance(event.widget, tk.Canvas):
            x = event.x / self.size
            y = event.y / self.size
            self._toggle_cell((x, y))

    def _toggle_cell(self, cell):
            x, y = cell
            if cell not in self.living_cells:
                x0 = x * self.size
                y0 = y * self.size
                x1 = x0 + self.size
                y1 = y0 + self.size
                id = self.canvas.create_rectangle(x0, y0, x1, y1,
                                                  width=0, fill='black')
                self.living_cells[cell] = id
                self.life.board[y][x] = 1
            else:
                self.canvas.delete(self.living_cells[cell])
                del self.living_cells[cell]
                self.life.board[y][x] = 0

    def start(self):
        self._running = True
        steps = self.scl_steps.get()
        delay = self._speeds[self.scl_speed.get()-1]
        for i in xrange(steps):
            if not self._running or not self.living_cells:
                break
            self.status.config(text = "Running %d/%d" % (i, steps))
            self.life.evolve()
            self.clear_screen()
            for x in xrange(self.width):
                for y in xrange(self.height):
                    if self.life.board[y][x] == 1:
                        self._toggle_cell((x, y))
            time.sleep(delay)
            self.canvas.update()
        self.status.config(text = "Idle")

    def stop(self):
        self._running = False

class Life(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in xrange(height)]

    def evolve(self):
        board_ = [[0] * self.width for _ in xrange(self.height)] # all dead
        for x in xrange(self.width):
            for y in xrange(self.height):
                v = self.board[y][x]
                n = self.get_neighbors((x, y))
                t = n.count(1)
                # Born or survive
                if (v == 0 and t == 3) or \
                   (v == 1 and t in (2, 3)):
                    board_[y][x] = 1
        self.board = board_
        return self.board

    def get_neighbors(self, cell):
        x_center, y_center = cell

        x_left  = x_center-1 if x_center-1 >= 0 else self.width-1
        x_right = x_center+1 if x_center+1 < self.width else 0
        y_up    = y_center-1 if y_center-1 >= 0 else self.height-1
        y_down  = y_center+1 if y_center+1 < self.height else 0

        return (self.board[y_up][x_left],
                self.board[y_up][x_center],
                self.board[y_up][x_right],
                self.board[y_center][x_left],
                self.board[y_center][x_right],
                self.board[y_down][x_left],
                self.board[y_down][x_center],
                self.board[y_down][x_right],)


if __name__ == '__main__':

    from optparse import OptionParser
    parser = OptionParser(description="Game of life")
    parser.add_option('-W', '--width', type=int, default=20,
                      help="board width (in cells)")
    parser.add_option('-H', '--height', type=int, default=20,
                      help="board height (in cells)")
    parser.add_option('-s', '--size', type=int, default=15,
                      help="cell size")
    args, _ = parser.parse_args()

    app = Application(args.width, args.height, args.size)
    app.master.title('Game of life')
    app.mainloop()

