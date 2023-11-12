import time
from pynput.keyboard import Key, Controller

class Player:
    def __init__(self, name):
        self.name = name
        self.keyboard = Controller()
        

    def left(self):
        self.keyboard.press(Key.left)
    
    def right(self):
        self.keyboard.press(Key.right)
    
    def up(self):
        self.keyboard.press(Key.up)
        
    def space(self):
        self.keyboard.press(Key.space)

    def newgame(self):
        self.keyboard.press(Key.enter)
        time.sleep(0.5)
        self.keyboard.press('n')
        time.sleep(0.5)
        self.keyboard.press(Key.enter)