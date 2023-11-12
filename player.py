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
        
    def down(self):
        self.keyboard.press(Key.down)

    