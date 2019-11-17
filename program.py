#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This program contains the main class 'Game' that instantiates a tkinter based
gui with a new round of the game '2048'. The whole business logic of the game
is included in this class.
The rules can be read at https://en.wikipedia.org/wiki/2048_(video_game).
"""

from tkinter import Tk, Toplevel, Label, Button, N, E, S, W
import random
import copy

class Game:
    """
    Main class that includes all methods that are required to start a new
    round of '2048' in a tkinter gui.
    """
    def __init__(self):
        """
        Method to get a new instance of the game class with a new gui window.
        """
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
        # window width x window height + position right + position down
        self.root.geometry("+300+300")
        self.root.title("2048")
        self.root.configure(background="AntiqueWhite3")
        self.root.mainloop()

    def key_return(self, event):
        """
        Handles the event that the return key is pressed within the popup
        window (if the game is over).
        """
        widget = self.popup.focus_get()
        btn_text = widget.config('text')[-1]
        if btn_text in ("Restart", "Quit"):
            widget.invoke()

    def key_pressed(self, direction):
        """
        Handles the event that an arrow key is pressed within the main window.
        """
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
        """
        Opens a popup window if the game is over to ask for a new game or to
        quit.
        """
        self.remove_bindings()
        self.popup = Toplevel(self.root)
        self.popup.wm_title("Game over")
        lbl = Label(self.popup, text="This game is over!", font=("Arial", 10))
        lbl.grid(row=0, column=0, columnspan=2, sticky=W+E+S, padx=100, pady=10)
        btn1 = Button(self.popup, text="Restart", font=("Arial", 10),
                      command=self.restart_game, width=10, bd=3)
        btn1.focus_set()
        btn1.grid(row=1, column=0, sticky=E+N, padx=10, pady=10)
        btn2 = Button(self.popup, text="Quit", font=("Arial", 10),
                      command=self.root.quit, width=10, bd=3)
        btn2.grid(row=1, column=1, sticky=W+N, padx=10, pady=10)
        self.popup.attributes('-topmost', True)
        self.popup.bind('<Return>', self.key_return)
        self.popup.geometry("+350+350")

    def restart_game(self):
        """
        Closes the popup window and starts a new round of the game in the main
        window.
        """
        self.get_start_field()
        self.get_labels()
        self.grid_labels()
        self.popup.unbind('<Return>')
        self.popup.destroy()
        self.popup.update()
        self.init_bindings()

    def zero_exists(self):
        """
        Checks whether there is at least one zero in the field.
        """
        for col in range(4):
            for row in range(4):
                if self.field[col][row] == 0:
                    return True
        return False

    def game_over(self):
        """
        Checks whether the game is over yet, i.e. there are no equivalent
        numbers adjacent to each other and furthermore there are no zeros
        (no free space) on the field.
        """
        for col in range(3):
            for row in range(4):
                if self.field[col][row] == self.field[col + 1][row]:
                    return False
        for col in range(4):
            for row in range(3):
                if self.field[col][row] == self.field[col][row + 1]:
                    return False
        return not self.zero_exists()

    def add_number(self):
        """
        Adds a 2 or a 4 to a random free coordinate on the field.
        """
        while True:
            col = random.randint(0, 3)
            row = random.randint(0, 3)
            if self.field[col][row] == 0:
                break
        self.field[col][row] = random.randint(1, 2) * 2

    @staticmethod
    def rotate_field_right_once(field):
        """
        Rotates the whole field 90 degrees to the right.
        """
        field_t = []
        for col in range(4):
            field_t.append([0, 0, 0, 0])
        for col in range(4):
            for row in range(4):
                field_t[row][3-col] = field[col][row]
        return field_t

    def rotate_field_right(self, field, direction, after_move=False):
        """
        Rotates the whole field multiple times to the right. The rotation is
        called recursively dependend on the direction (the arrow key that was
        pressed). If the optional parameter 'after_move' is True, the rotation
        is called after moving the numbers to the right, i.e. the field was
        rotated before the move already and has to be rotated to its original
        orientation now. While the direction equals the key that was initially
        pressed, the number of rotation changes if after_move is True.
        """
        if after_move and direction in ("u", "d"):
            direction = "u" if direction == "d" else "d"
        rotations_to_go = self.directions[direction]
        if rotations_to_go == 0:
            return field
        field_rotated = self.rotate_field_right_once(field)
        directions = {y:x for x, y in self.directions.items()}
        return self.rotate_field_right(field_rotated,
                                       directions[rotations_to_go - 1])

    def get_next_field(self, direction):
        """
        Calculates the next field after moving all numbers to a given
        direction. The central logic for moving and merging the numbers on
        the field is written for the case, that direction is equal to 'r'
        (right). If the direction is not equal to 'r', the field is rotated,
        then the moving and merging is executed on the rotated field and
        finally the field is rotated again to its original orientation.
        If the new field is different to the input field, the function returns
        True and updates the field variable of the game class.
        """
        field = copy.copy(self.field)
        field = self.rotate_field_right(field, direction)
        field = self.move_field_right(field)
        field = self.rotate_field_right(field, direction, True)
        if field == self.field:
            return False
        self.field = field
        return True

    def move_field_right(self, field):
        """
        Move all numbers of the given field to the right direction and merge
        adjacent equivalent numbers. Calculate the new field row by row
        (divide & conquer).
        """
        for row in range(4):
            field[row] = self.move_row_right(field[row])
        return field

    @staticmethod
    def move_row_right(row):
        """
        Move all numbers of the given row to the right direction and merge
        adjacent equivalent numbers.
        """
        row_new = []
        for col in range(3, -1, -1):
            if row[col] != 0:
                row_new.append(row[col])
        while len(row_new) != 4:
            row_new.append(0)
        row_new = list(reversed(row_new))
        if row_new[2] == row_new[3]:
            row_new[3] *= 2
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
            row_new[2] *= 2
        elif row_new[0] == row_new[1]:
            row_new[1] *= 2
            row_new[0] = 0
        return row_new

    def quit(self, event):
        """
        Quits the application.
        """
        self.root.destroy()

    def init_bindings(self):
        """
        Initializes the bindings for all keys that have a correspondent
        function.
        """
        self.root.bind('<Escape>', self.quit)
        self.root.bind('<Left>', lambda event, k="l": self.key_pressed(k))
        self.root.bind('<Right>', lambda event, k="r": self.key_pressed(k))
        self.root.bind('<Up>', lambda event, k="u": self.key_pressed(k))
        self.root.bind('<Down>', lambda event, k="d": self.key_pressed(k))

    def remove_bindings(self):
        """
        Removes all bindings (except the escape command) to freeze the main
        window if the game is over.
        """
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')
        self.root.unbind('<Up>')
        self.root.unbind('<Down>')

    def get_start_field(self):
        """
        Returns a new field with 4 numbers height and width filled with zeros
        and two random numbers.
        """
        field = []
        for col in range(4):
            field.append([])
            for _ in range(4):
                field[col].append(0)
        self.field = field
        for _ in range(2):
            self.add_number()

    def get_labels(self):
        """
        Updates the dict of the main class that contains one label for each
        number of the field. Each label is saved with the name 'l00' where the
        first digit is the row and the second digit is the column of the
        label. After updating the labels they can be rendered via the grid
        function.
        """
        labels = {}
        for col in range(4):
            for row in range(4):
                font = ("Arial", 20)
                height = 2
                width = 4
                if self.field[col][row] == 0:
                    labels["l" + str(col) + str(row)] = Label(
                        self.root, fg=self.colors[0], bg=self.colors[0],
                        text="0", font=font, height=height, width=width)
                else:
                    labels["l" + str(col) + str(row)] = Label(
                        self.root, bg=self.colors[min(
                            self.field[col][row], list(self.colors.keys())[-1])],
                        text=str(self.field[col][row]), font=font, height=height,
                        width=width)
        self.labels = labels

    def grid_labels(self):
        """
        Updates the grid and places all labels of the dict into the grid at
        the position that is given with the dictionarys keys.
        """
        for row in range(4):
            for col in range(4):
                self.labels["l" + str(row) + str(col)].grid(
                    row=row, column=col, padx=3, pady=3)

if __name__ == "__main__":
    GAME = Game()
