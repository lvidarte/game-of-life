#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import Tkinter as tk

from patterns import patterns


class Application(tk.Frame):

    def __init__(self, width, height, size=10):
        tk.Frame.__init__(self)
        self.grid()
        self.width = width
        self.height = height
        self.size = size
        self.cells_alive = {}
        self.delays = [i/10.0 for i in range(1, 11)][::-1]
        self.delays[-1] = 0
        self.create_widgets()
        self.init_life()
        self.draw_grid()
        self.create_events()

    def init_life(self):
        self.life = Life(self.width, self.height)
        self.clear_screen()
        self.running = False

    def clear_screen(self):
        for id in self.cells_alive.values():
            self.canvas.delete(id)
        self.cells_alive = {}

    def create_widgets(self):
        width = self.width * self.size
        height = self.height * self.size
        self.canvas = tk.Canvas(self, width=width, height=height, bg='white')
        self.canvas.grid(row=0, column=0)

        self.status = tk.Label(self, text="click to add or remove cells")
        self.status.grid(row=1, column=0)

        self.sidebar = tk.Frame()
        self.sidebar.grid(row=0, column=1, rowspan=2, sticky=tk.N)

        self.scl_steps = tk.Scale(self.sidebar, from_=1, to=500,
                                  label='steps', orient=tk.HORIZONTAL)
        self.scl_steps.grid()
        self.scl_steps.set(1)

        self.scl_speed = tk.Scale(self.sidebar, from_=1, to=10,
                                  label='speed', orient=tk.HORIZONTAL)
        self.scl_speed.grid()
        self.scl_speed.set(9)
 
        self.btn_go = tk.Button(self.sidebar, text="Go", command=self.go)
        self.btn_go.grid()

        self.btn_stop = tk.Button(self.sidebar, text="Stop", command=self.stop)
        self.btn_stop.grid()

        self.btn_reset = tk.Button(self.sidebar, text="Reset",
                                  command=self.init_life)
        self.btn_reset.grid()

        self.pattern = tk.StringVar(self.sidebar)
        self.pattern.set(patterns.keys()[0])
        self.opt_patterns = tk.OptionMenu(self.sidebar,
                                          self.pattern,
                                          *patterns.keys())
        self.opt_patterns.grid()


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
        self.canvas.bind_all('<Button-1>', self.draw)

    def draw(self, event):
        if isinstance(event.widget, tk.Canvas):
            x = event.x / self.size
            y = event.y / self.size
            pattern = patterns[self.pattern.get()]
            if pattern is None:
                self.toggle_cell((x, y))
            else:
                self.toggle_pattern((x, y), pattern)

    def toggle_cell(self, cell):
        if cell in self.cells_alive:
            self.del_cell(cell)
        else:
            self.draw_cell(cell)

    def toggle_pattern(self, cell, pattern):
        if self.pattern_in_cells_alive(cell, pattern):
            self.del_pattern(cell, pattern)
        else:
            self.draw_pattern(cell, pattern)

    def pattern_in_cells_alive(self, cell, pattern):
        x, y = cell
        for x0 in xrange(len(pattern[0])):
            for y0 in xrange(len(pattern)):
                x1 = (x + x0) % self.width
                y1 = (y + y0) % self.height
                if pattern[y0][x0] == 1 and \
                   (x1, y1) not in self.cells_alive:
                    return False
        return True

    def draw_cell(self, cell):
        x, y = cell
        x0 = x * self.size
        y0 = y * self.size
        x1 = x0 + self.size
        y1 = y0 + self.size
        id = self.canvas.create_rectangle(x0, y0, x1, y1,
                                          width=0, fill='black')
        self.cells_alive[cell] = id
        self.life.set(cell, 1)

    def del_cell(self, cell):
        x, y = cell
        self.canvas.delete(self.cells_alive[cell])
        del self.cells_alive[cell]
        self.life.set(cell, 0)

    def draw_pattern(self, cell, pattern):
        x, y = cell
        for x0 in xrange(len(pattern[0])):
            for y0 in xrange(len(pattern)):
                x1 = (x + x0) % self.width
                y1 = (y + y0) % self.height
                if pattern[y0][x0] == 1 and not (x1, y1) in self.cells_alive:
                    self.draw_cell((x1, y1))

    def del_pattern(self, cell, pattern):
        x, y = cell
        for x0 in xrange(len(pattern[0])):
            for y0 in xrange(len(pattern)):
                x1 = (x + x0) % self.width
                y1 = (y + y0) % self.height
                if pattern[y0][x0] == 1 and (x1, y1) in self.cells_alive:
                    self.del_cell((x1, y1))

    def go(self):
        self.running = True
        steps = self.scl_steps.get()
        delay = self.delays[self.scl_speed.get()-1]
        for i in xrange(steps):
            if not self.running or not self.cells_alive:
                break
            self.status.config(text = "Running %d/%d" % (i, steps))
            self.life.evolve()
            self.clear_screen()
            for x in xrange(self.width):
                for y in xrange(self.height):
                    if self.life.get((x, y)) == 1:
                        self.toggle_cell((x, y))
            time.sleep(delay)
            self.canvas.update()
        self.status.config(text = "Idle")

    def stop(self):
        self.running = False

class Life(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.world = [[0] * width for _ in xrange(height)]

    def evolve(self):
        world_ = [[0] * self.width for _ in xrange(self.height)] # all dead
        for x in xrange(self.width):
            for y in xrange(self.height):
                v = self.world[y][x]
                n = self.get_neighbors((x, y))
                t = n.count(1)
                # Born or survive
                if (v == 0 and t == 3) or \
                   (v == 1 and t in (2, 3)):
                    world_[y][x] = 1
        self.world = world_
        return self.world

    def get_neighbors(self, cell):
        x_center, y_center = cell

        x_left  = x_center-1 if x_center-1 >= 0 else self.width-1
        x_right = x_center+1 if x_center+1 < self.width else 0
        y_up    = y_center-1 if y_center-1 >= 0 else self.height-1
        y_down  = y_center+1 if y_center+1 < self.height else 0

        return (self.get((x_left, y_up)),
                self.get((x_center, y_up)),
                self.get((x_right, y_up)),
                self.get((x_left, y_center)),
                self.get((x_right, y_center)),
                self.get((x_left, y_down)),
                self.get((x_center, y_down)),
                self.get((x_right, y_down)),)

    def set(self, cell, value):
        x, y = cell
        self.world[y][x] = value

    def get(self, cell):
        x, y = cell
        return self.world[y][x]


if __name__ == '__main__':

    from optparse import OptionParser
    parser = OptionParser(description="Game of life")
    parser.add_option('-W', '--width', type=int, default=20,
                      help="world width (in cells)")
    parser.add_option('-H', '--height', type=int, default=20,
                      help="world height (in cells)")
    parser.add_option('-s', '--size', type=int, default=15,
                      help="cell size")
    args, _ = parser.parse_args()

    app = Application(args.width, args.height, args.size)
    app.master.title('Game of life')
    app.mainloop()

