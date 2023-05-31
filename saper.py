import tkinter as tk
import random
import time
import sys
import os

WIDTH, HEIGHT, MINES = 8, 8, 10


class Mine(tk.Button):
    def __init__(self, parent, x: int, y: int):
        super().__init__(parent, width=2, height=1, font=(
            'Segoe UI', 12, 'bold'), command=self.open_place)
        # self.bind("<Button-1>", self.open_place)
        self.bind("<Button-2>", self.flag_place)
        self.bind("<Button-3>", self.flag_place)
        self.x, self.y = x, y
        self.flagged = False
        self.opened = False

    def add(self):
        self.grid(column=self.x, row=self.y)

    def open_place(self):
        global game_over, mines, start_time
        if mines is not None:
            if not self.opened and not self.flagged and not game_over:
                neighbors = self.get_neighbors()
                self.opened = True
                if mines[self.y][self.x]:
                    game_over = True
                    clock_label.config(fg='red')
                    end_game()
                elif neighbors != 0:
                    self.config(text=str(neighbors))
                    if neighbors == 1:
                        self.config(fg='blue', activeforeground='blue')
                    elif neighbors == 2:
                        self.config(fg='green', activeforeground='green')
                    elif neighbors == 3:
                        self.config(fg='red', activeforeground='red')
                    elif neighbors == 4:
                        self.config(fg='purple', activeforeground='purple')
                    else:
                        self.config(fg='orange', activeforeground='orange')
                else:
                    self.config(text='')
                    if self.x - 1 >= 0:
                        if not buttons[self.y][self.x - 1].opened:
                            buttons[self.y][self.x - 1].open_place()
                    if self.y - 1 >= 0:
                        if not buttons[self.y - 1][self.x].opened:
                            buttons[self.y - 1][self.x].open_place()
                    if self.x + 1 < len(mines):
                        if not buttons[self.y][self.x + 1].opened:
                            buttons[self.y][self.x + 1].open_place()
                    if self.y + 1 < len(mines[0]):
                        if not buttons[self.y + 1][self.x].opened:
                            buttons[self.y + 1][self.x].open_place()
                    if self.x - 1 >= 0 and self.y - 1 >= 0:
                        if not buttons[self.y - 1][self.x - 1].opened:
                            buttons[self.y - 1][self.x - 1].open_place()
                    if self.x - 1 >= 0 and self.y + 1 < len(mines[0]):
                        if not buttons[self.y + 1][self.x - 1].opened:
                            buttons[self.y + 1][self.x - 1].open_place()
                    if self.x + 1 < len(mines) and self.y - 1 >= 0:
                        if not buttons[self.y - 1][self.x + 1].opened:
                            buttons[self.y - 1][self.x + 1].open_place()
                    if self.x + 1 < len(mines) and self.y + 1 < len(mines[0]):
                        if not buttons[self.y + 1][self.x + 1].opened:
                            buttons[self.y + 1][self.x + 1].open_place()
                self.config(relief='sunken')

                not_mined_closed = False
                for line in buttons:
                    for mine in line:
                        if not mine.opened and not mines[mine.y][mine.x]:
                            not_mined_closed = True
                if not not_mined_closed:
                    game_over = True
                    clock_label.config(fg='green')
                    end_game()
        else:
            mines = prepare_board(WIDTH, HEIGHT, MINES, self.x, self.y)
            start_time = time.time()
            self.open_place()
            root.after(100, update_clock)

    def flag_place(self, e):
        global flags
        if not self.opened and not game_over:
            if not self.flagged:
                self.config(text='F')
                self.flagged = True
                flags += 1
            else:
                self.config(text='')
                self.flagged = False
                flags -= 1
            mines_label.config(text=str(MINES - flags))

    def get_neighbors(self):
        neighbors = 0
        if self.x - 1 >= 0:
            neighbors += int(mines[self.y][self.x - 1])
        if self.x + 1 < len(mines):
            neighbors += int(mines[self.y][self.x + 1])
        if self.y - 1 >= 0:
            neighbors += int(mines[self.y - 1][self.x])
        if self.y + 1 < len(mines[0]):
            neighbors += int(mines[self.y + 1][self.x])
        if self.x - 1 >= 0 and self.y - 1 >= 0:
            neighbors += int(mines[self.y - 1][self.x - 1])
        if self.x - 1 >= 0 and self.y + 1 < len(mines[0]):
            neighbors += int(mines[self.y + 1][self.x - 1])
        if self.x + 1 < len(mines) and self.y - 1 >= 0:
            neighbors += int(mines[self.y - 1][self.x + 1])
        if self.x + 1 < len(mines) and self.y + 1 < len(mines[0]):
            neighbors += int(mines[self.y + 1][self.x + 1])
        return neighbors


def end_game():
    for y, line in enumerate(mines):
        for x, mine in enumerate(line):
            if mine:
                buttons[y][x].config(text='M')


def prepare_board(w, h, m, cx, cy):
    board = [[False for _ in range(w)] for _ in range(h)]
    while sum([line.count(True) for line in board]) != m:
        x, y = random.randint(0, w - 1), random.randint(0, h - 1)
        if (cx, cy) != (x, y) \
                and (cx, cy) != (x - 1, y) and (cx, cy) != (x, y - 1) \
                and (cx, cy) != (x + 1, y) and (cx, cy) != (x, y + 1) \
                and (cx, cy) != (x - 1, y - 1) and (cx, cy) != (x + 1, y + 1) \
                and (cx, cy) != (x - 1, y + 1) and (cx, cy) != (x + 1, y - 1):
            board[y][x] = True
    return board


def update_clock():
    if not game_over:
        clock_label.config(text=str(int(time.time() - start_time)))
        root.after(100, update_clock)


game_over = False
mines = None
flags = 0

root = tk.Tk()
root.title('Saper')
if getattr(sys, 'frozen', False):
    root.iconbitmap(os.path.join(sys._MEIPASS, "elephant.ico"))
else:
    root.iconbitmap('elephant.ico')

root.resizable(0, 0)

top_frame = tk.Frame(root)

clock_label = tk.Label(top_frame, text='0', font=('Segoe UI', 12, 'bold'))
clock_label.grid(column=0, row=0)

margin_label = tk.Label(top_frame, width=2, font=('Segoe UI', 12, 'bold'))
margin_label.grid(column=1, row=0)

mines_label = tk.Label(top_frame, text=str(
    MINES), font=('Segoe UI', 12, 'bold'))
mines_label.grid(column=2, row=0)

top_frame.pack()

frame = tk.Frame(root)
frame.pack()

buttons = []

for y in range(HEIGHT):
    buttons_line = []
    for x in range(WIDTH):
        mine = Mine(frame, x, y)
        mine.add()
        buttons_line.append(mine)
    buttons.append(buttons_line)

start_time = None

root.mainloop()
