import player
from game import Game
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque


gam = Game()

gam.startNewGame()
