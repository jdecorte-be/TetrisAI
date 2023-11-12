import player
from game import Game
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
from PIL import ImageGrab
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()


g = Game()

# gam.startNewGame()
# while True:
time.sleep(2)

keyboard.press('n')
screen = ImageGrab.grab()
screen = np.array(screen)

img = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
g.detectBoard(img)
g.getPiece()
g.getNextState()
# g.step(({"x": 0, "y": 0}, 2))
