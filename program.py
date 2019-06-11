#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
TODO: docstrings
"""

from tkinter import *
import random, copy

class game:
    def __init__(self):
        self.root = Tk()
        self.colors = {0:"AntiqueWhite2", 2:"AntiqueWhite1", 4:"bisque2",
                       8:"sandy brown", 16:"chocolate1", 32:"tomato",
                       64:"orange red", 128:"light goldenrod",
                       256:"light goldenrod", 512:"light goldenrod",
                       1024:"yellow2", 2048:"gold"}
        self.directions = {"d": 3, "l": 2, "u": 1, "r": 0}
        self.get_start_field()
        self.get_labels()
        self.grid_labels()

        self.init_bindings()
        #window width x window height + position right + position down
        self.root.geometry("+300+300")
        self.root.title("2048")
        self.root.configure(background="AntiqueWhite3")
        self.root.mainloop()

    def key_return(self,event):
        widget = self.popup.focus_get()
        btn_text = widget.config('text')[-1]
        if btn_text == "Restart" or btn_text == "Quit":
            widget.invoke()

    def key_pressed(self, direction):
        if self.get_next_field(direction):
            if not self.zero_exists():
                self.show_popup()
            else:
                self.add_number()
                self.get_labels()
                self.grid_labels()
                if self.game_over():
                    self.show_popup()

    def show_popup(self):
        self.remove_bindings()
        self.popup = Toplevel(self.root)
        self.popup.wm_title("Game over")
        l = Label(self.popup, text="This game is over!", font = ("Arial", 10))
        l.grid(row=0, column=0, columnspan=2, sticky=W+E+S, padx=100, pady=10)
        b1 = Button(self.popup, text="Restart", font = ("Arial", 10),
                    command=self.restart_game, width=10, bd=3)
        b1.focus_set()
        b1.grid(row=1, column=0, sticky=E+N, padx=10, pady=10)
        b2 = Button(self.popup, text="Quit", font = ("Arial", 10),
                    command=self.root.quit, width=10, bd=3)
        b2.grid(row=1, column=1, sticky=W+N, padx=10, pady=10)
        self.popup.attributes('-topmost', True)
        self.popup.bind('<Return>', self.key_return)
        self.popup.geometry("+350+350")

    def restart_game(self):
        self.get_start_field()
        self.get_labels()
        self.grid_labels()
        self.popup.unbind('<Return>')
        self.popup.destroy()
        self.popup.update()
        self.init_bindings()

    def zero_exists(self):
        for x in range(4):
            for y in range(4):
                if self.field[x][y] == 0:
                    return True
        return False
    
    def game_over(self):
        for x in range(3):
            for y in range(4):
                if self.field[x][y] == self.field[x + 1][y]:
                    return False
        for x in range(4):
            for y in range(3):
                if self.field[x][y] == self.field[x][y + 1]:
                    return False
        return not self.zero_exists()

    def add_number(self):
        while True:
            x = random.randint(0,3)
            y = random.randint(0,3)
            if self.field[x][y] == 0:
                break
        self.field[x][y] = random.randint(1, 2) * 2

    def rotate_field_right_once(self, field):
        field_t = []
        for x in range(4):
            field_t.append([0,0,0,0])
        for x in range(4):
            for y in range(4):
                field_t[y][3-x] = field[x][y]
        return field_t

    def rotate_field_right(self, field, direction, after_move = False):
        if after_move and (direction == "u" or direction == "d"):
            direction = "u" if direction == "d" else "d"
        rotations_to_go = self.directions[direction]
        if rotations_to_go == 0:
            return field
        else:
            field_rotated = self.rotate_field_right_once(field)
            directions = {y:x for x,y in self.directions.items()}
            return self.rotate_field_right(field_rotated,
                directions[rotations_to_go - 1])

    def get_next_field(self, direction):
        field = copy.copy(self.field)
        field = self.rotate_field_right(field, direction)
        field = self.move_field_right(field)
        field = self.rotate_field_right(field, direction, True)
        
        if field == self.field:
            return False
        else:
            self.field = field
            return True

    def move_field_right(self, field):
        for row in range(4):
            field[row] = self.move_row_right(field[row])
        return field

    def move_row_right(self, row):
        row_new = []
        for col in range(3,-1,-1):
            if row[col] != 0:
                row_new.append(row[col])
        while len(row_new) != 4:
            row_new.append(0)
        row_new = list(reversed(row_new))
        if row_new[2] == row_new[3]:
            row_new[3] = row_new[3] * 2
            if row_new[0] == row_new[1]:
                row_new[2] = row_new[1] * 2
                row_new[1] = 0
            else:
                row_new[2] = row_new[1]
                row_new[1] = row_new[0]
            row_new[0] = 0
        elif row_new[1] == row_new[2]:
            row_new[1] = row_new[0]
            row_new[0] = 0
            row_new[2] = row_new[2] * 2
        elif row_new[0] == row_new[1]:
            row_new[1] = row_new[1] * 2
            row_new[0] = 0
        return row_new
    
    def quit(self,event):
        self.root.destroy()

    def init_bindings(self):
        self.root.bind('<Escape>', self.quit)
        self.root.bind('<Left>', lambda event, k="l": self.key_pressed(k))
        self.root.bind('<Right>', lambda event, k="r": self.key_pressed(k))
        self.root.bind('<Up>', lambda event, k="u": self.key_pressed(k))
        self.root.bind('<Down>', lambda event, k="d": self.key_pressed(k))

    def remove_bindings(self):
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')
        self.root.unbind('<Up>')
        self.root.unbind('<Down>')

    def get_start_field(self):
        field = []
        for x in range(4):
            field.append([])
            for y in range(4):
                field[x].append(0)
        self.field = field
        for x in range(2):
            self.add_number()

    def get_labels(self):
        labels = {}
        for x in range(4):
            for y in range(4):
                font = ("Arial", 20)
                height = 2
                width = 4
                if self.field[x][y] == 0:
                    labels["l" + str(x) + str(y)] = Label(self.root,
                        fg = self.colors[0],
                        bg = self.colors[0], text="0",
                        font = font, height = height, width = width)
                else:
                    labels["l" + str(x) + str(y)] = Label(self.root,
                        bg = self.colors[min(self.field[x][y],
                                             list(self.colors.keys())[-1])],
                        text=str(self.field[x][y]),
                        font = font, height = height, width = width)
        self.labels = labels

    def grid_labels(self):
        for x in range(4):
            for y in range(4):
                self.labels["l" + str(x) + str(y)].grid(row=x, column=y, padx=3, pady=3)

if __name__ == "__main__":
    g = game()
