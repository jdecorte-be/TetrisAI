"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""
import argparse
import numpy as np
import torch
import cv2
from game import Game
from pynput.keyboard import Key, Controller
from PIL import ImageGrab

import time
keyboard = Controller()


def get_args():
    parser = argparse.ArgumentParser(
        """Implementation of Deep Q Network to play Tetris""")

    parser.add_argument("--width", type=int, default=10, help="The common width for all images")
    parser.add_argument("--height", type=int, default=20, help="The common height for all images")
    parser.add_argument("--block_size", type=int, default=30, help="Size of a block")
    parser.add_argument("--fps", type=int, default=300, help="frames per second")
    parser.add_argument("--saved_path", type=str, default="trained_models")
    parser.add_argument("--output", type=str, default="output.mp4")

    args = parser.parse_args()
    return args


def test(opt):
    if torch.cuda.is_available():
        torch.cuda.manual_seed(123)
    else:
        torch.manual_seed(123)
    if torch.cuda.is_available():
        model = torch.load("{}/tetris".format(opt.saved_path))
    else:
        model = torch.load("{}/tetris".format(opt.saved_path), map_location=lambda storage, loc: storage)
    model.eval()
    env = Game()
    
    env.reset()
    if torch.cuda.is_available():
        model.cuda()
    
    time.sleep(1)
    keyboard.press('n')
    while True:
        screen = ImageGrab.grab()
        screen = np.array(screen)
        img = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        env.detectBoard(img)
        env.getPiece()
        
        next_steps = env.getNextState()
        next_actions, next_states = zip(*next_steps.items())
        next_states = torch.stack(next_states)
        if torch.cuda.is_available():
            next_states = next_states.cuda()
        predictions = model(next_states)[:, 0]
        index = torch.argmax(predictions).item()
        action = next_actions[index]
        print(action)
        _, done = env.step(action)

        if done:
            break
        
    keyboard.press("A")
    keyboard.press("9")
    keyboard.press(Key.enter)

if __name__ == "__main__":
    opt = get_args()
    test(opt)
