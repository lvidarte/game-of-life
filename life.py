"""
Author: Leo Vidarte <http://nerdlabs.com.ar>

This is free software,
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.

"""

import time
import tkinter as tk

from patterns import patterns


STEPS = ['1', '5', '10', '50', '100', '500', 'forever']
SLEEPS = [0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]


class Application(tk.Frame):

    def __init__(self, width, height, size=10):
        tk.Frame.__init__(self)
        self.grid()
        self.width = width
        self.height = height
        self.size = size
        self.cells_alive = {}
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

        sidebar = self.sidebar = tk.Frame()
        sidebar.grid(row=0, column=1, rowspan=2,
                     sticky=tk.N, padx=10, pady=10)

        tk.Label(sidebar, text='Steps').grid()

        self.steps = tk.StringVar()
        self.steps.set(STEPS[0])
        opt_steps = self.opt_steps = tk.OptionMenu(
                sidebar, self.steps, *STEPS)
        opt_steps.grid()

        tk.Label(sidebar, text='Sleep (sec)').grid()

        self.sleep = tk.StringVar()
        self.sleep.set(SLEEPS[3])
        opt_sleep = self.opt_sleep = tk.OptionMenu(
                sidebar, self.sleep, *SLEEPS)
        opt_sleep.grid()

        separator = tk.Frame(sidebar, height=2, bd=1, relief=tk.SUNKEN)
        separator.grid(sticky=tk.E+tk.W, padx=5, pady=10)

        self.btn_run = tk.Button(sidebar, text="Run", command=self.run)
        self.btn_run.grid()

        self.btn_stop = tk.Button(sidebar, text="Stop", command=self.stop)
        self.btn_stop.grid()

        self.btn_clear = tk.Button(sidebar, text="Clear",
                                   command=self.init_life)
        self.btn_clear.grid()

        separator = tk.Frame(sidebar, height=2, bd=1, relief=tk.SUNKEN)
        separator.grid(sticky=tk.E+tk.W, padx=5, pady=10)

        btn_patterns = self.btn_patterns = tk.Button(
                sidebar, text="Patterns", command=self.show_patterns)
        btn_patterns.grid()

        # ---------------
        # Patterns Window
        # ---------------
        win_patterns = self.win_patterns = tk.Toplevel(self)
        win_patterns.title('Patterns')
        win_patterns.rowconfigure(0, weight=1)
        win_patterns.columnconfigure(0, weight=1)

        scrollbar = tk.Scrollbar(win_patterns, orient=tk.VERTICAL)
        scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)

        lst_patterns = self.lst_patterns = tk.Listbox(
                win_patterns, yscrollcommand=scrollbar.set,
                height=20, width=30)
        for item in patterns.keys():
            lst_patterns.insert(tk.END, item)
        lst_patterns.selection_set(0)

        scrollbar.config(command=lst_patterns.yview)
        lst_patterns.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        win_patterns.protocol("WM_DELETE_WINDOW", self.save_top)
        #win_patterns.withdraw()

    def save_top(self):
        self.win_patterns.withdraw()

    def show_patterns(self):
        self.win_patterns.deiconify()

    def draw_grid(self):
        color = 'gray'
        for i in range(self.width - 1):
            x = (self.size * i) + self.size
            y0 = 0
            y1 = self.size * self.height
            self.canvas.create_line(x, y0, x, y1, fill=color)
        for i in range(self.height - 1):
            x0 = 0
            x1 = self.size * self.width
            y = (self.size * i) + self.size
            self.canvas.create_line(x0, y, x1, y, fill=color)

    def create_events(self):
        self.canvas.bind_all('<Button-1>', self.draw)

    def draw(self, event):
        if isinstance(event.widget, tk.Canvas):
            x = event.x // self.size
            y = event.y // self.size
            items = self.lst_patterns.curselection()
            pattern = patterns[self.lst_patterns.get(items[0])]
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
        for x0 in range(len(pattern[0])):
            for y0 in range(len(pattern)):
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
        for x0 in range(len(pattern[0])):
            for y0 in range(len(pattern)):
                x1 = (x + x0) % self.width
                y1 = (y + y0) % self.height
                if pattern[y0][x0] == 1 and not (x1, y1) in self.cells_alive:
                    self.draw_cell((x1, y1))

    def del_pattern(self, cell, pattern):
        x, y = cell
        for x0 in range(len(pattern[0])):
            for y0 in range(len(pattern)):
                x1 = (x + x0) % self.width
                y1 = (y + y0) % self.height
                if pattern[y0][x0] == 1 and (x1, y1) in self.cells_alive:
                    self.del_cell((x1, y1))

    def run(self):
        self.running = True
        steps = self.steps.get()
        self.opt_steps.config(state=tk.DISABLED)
        if steps == 'forever':
            step = 1
            while self.running and self.cells_alive:
                self._run(step, steps)
                step += 1
        else:
            for step in range(int(steps)):
                if not self.running or not self.cells_alive:
                    break
                self._run(step, steps)
        self.status.config(text = "Idle")
        self.opt_steps.config(state=tk.NORMAL)

    def _run(self, step, steps):
        self.status.config(text = "Running %s/%s" % (step, steps))
        self.life.evolve()
        self.clear_screen()
        for x in range(self.width):
            for y in range(self.height):
                if self.life.get((x, y)) == 1:
                    self.toggle_cell((x, y))
        self.canvas.update()
        time.sleep(float(self.sleep.get()))

    def stop(self):
        self.running = False

class Life(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.world = [[0] * width for _ in range(height)]

    def evolve(self):
        world_ = [[0] * self.width for _ in range(self.height)] # all dead
        for x in range(self.width):
            for y in range(self.height):
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
    parser.add_option('-W', '--width', type=int, default=80,
                      help="world width (default: 80)")
    parser.add_option('-H', '--height', type=int, default=40,
                      help="world height (default: 40)")
    parser.add_option('-s', '--size', type=int, default=20,
                      help="cell size (default: 20)")
    args, _ = parser.parse_args()

    app = Application(args.width, args.height, args.size)
    app.master.title('Game of life')
    app.mainloop()

