import torch
import random
from pynput.keyboard import Key, Controller
import numpy as np
from game import Game

matrix = [
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 1., 1., 1., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
]

keyboard = Controller()
class Train:
    def __init__(self):
        self.matrix = matrix #a changer par detection
        self.reward = 0
        self.coordonnee = [self.matrix[4][5], self.matrix[4][6], self.matrix[4][4]] #a changer par detection
        self.moves = [self.right(), self.left(), self.up(), self.down(), self.space()]

    def debut_train(self):
        random.shuffle(self.moves)
        self.moves[0]

    def mid_train(self):
        # Perform some actions in the middle of training
        self.right()
        self.left()
        self.up()
        self.down()
        self.space()

    def background_train(self):
        self.debut_train()  # Shuffle and perform an action
        self.penality()  # Simulate a penalty scenario

    def penality(self):
        for i in range(len(self.matrix)-1, 0, -1):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 1:
                    self.reward += 5
                    return 1
                else : 
                    self.reward -= 1
                    return 0
            

    def Architecture(self, action):
        self.state = self.matrix
        self.moves[action]

    def right(self):
        keyboard.press('right')
        for i in range (len(self.coordonnee)):
            for j in range (len(self.coordonne[i])):
                self.coordonne[i][j] = self.coordonne[i][j] + 1
    def left(self):
        keyboard.press('left')
        for i in range (len(self.coordonnee)):
            for j in range (len(self.coordonne[i])):
                self.coordonne[i][j] = self.coordonne[i][j] - 1
    def up(self):
        keyboard.press('up')
        #rotate()
        self.piece = Game.piece
        curr_piece = np.array(self.piece)
        curr_piece = np.rot90(curr_piece, 1)
    def down(self):
        keyboard.press('down')
        for i in range (len(self.coordonnee)):
            self.coordonne[i] = self.coordonne[i] - 1
    def space(self):
        keyboard.press('space')
        for i in range (len(self.coordonnee)):
            self.coordonne[i] = self.coordonne[i] - 1
        while self.coordonnee != 1:
            self.coordonne[i] = self.coordonne[i] - 1
        for i in range (len(self.coordonnee)):
            for j in range (len(self.coordonne[i])):
                self.coordonne[i][j] = 1