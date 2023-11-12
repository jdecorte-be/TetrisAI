from pynput.keyboard import Key, Controller
import time 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from enum import Enum
from game import Game

keyboard = Controller()
driver = webdriver.Chrome()
driver.get(driver.current_url)

matrix = [
    [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
    [1., 1., 0., 0., 0., 0., 0., 0., 0., 1., 1., 1.],
    [1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
    [1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
]

class Direction (Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    SPACE = 4

class Tetrisgame:
    def __init__(self):
        self.board = matrix
        self.direction = Direction.SPACE
        self.reward = 0
        self.game = True

    def get_height(self):
        # Iterate through the rows from the top and find the first non-empty row
        for row_index, row in enumerate(self.board):
            if any(row):
                # Return the height as the index of the first non-empty row
                return row_index

        # If the grid is completely empty, return the full height
        return len(self.board)

    def game_over(self):
        try:
            # Use an appropriate condition to wait for the presence of an alert
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            # If an alert is present, handle it
            print("Alert detected!")
            print("Alert text:", alert.text)
            self.game = False
            self.reward -=10
        except TimeoutException:
            print("No alert detected.")
            self.reward+=3

    def move(self, action):
        if action == Direction.RIGHT:
            keyboard.press('right')
        elif action == Direction.LEFT:
            keyboard.press('left')
        elif action == Direction.UP:
            keyboard.press('up')
        elif action == Direction.SPACE:
            keyboard.press('space')

    def play(self, action):
        while self.game:
            self.move(action)
            time.sleep(0.1)
            self.game_over()
        self.reset()

    def reset(self):
        self.game = True
        keyboard.press('enter')
        keyboard.press('n')
        keyboard.press('enter')

if __name__ == '__main__':
    tetris = Tetrisgame()
    tetris.play(Direction.RIGHT)