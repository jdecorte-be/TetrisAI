import player
import cv2
import numpy as np
from PIL import ImageGrab
import pywinctl as pwc
import time
import subprocess
import pytesseract
import easyocr

class Game:
    
    def __init__(self):
        print("Game started")
        self.Player = player.Player("Les Hackathon")
        self.board = np.zeros((22, 12))
        self.piece_id = 0
    

    def getPiece(self):
        piece = np.zeros((3, 3))

        # get type of piece
        for i in range(3):
            for j in range(3):
                piece[i][j] = int(self.board[i][j + 4])
        
        all_piece = {
            "s": [[0,1,1],[1,1,0],[0,0,0]],
            "z": [[1,1,0],[0,1,1],[0,0,0]],
            "j": [[1,0,0],[1,1,1],[0,0,0]],
            "l": [[0,0,1],[1,1,1],[0,0,0]],
            "o": [[0,1,1],[0,1,1],[0,0,0]],
            "i": [[1,1,1],[0,0,0],[0,0,0]],
            "t": [[0,1,0],[1,1,1],[0,0,0]]
        }
        
        for key, value in all_piece.items():
            if (piece == value).all():
                self.piece_id = key
                
        print(self.piece_id)
        
    def startNewGame(self):
        while True:
            self.board = np.zeros((22, 12))
            screen = ImageGrab.grab()
            screen = np.array(screen)
            img = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            self.detectBoard(img)
            self.getPiece()
            
    
    def detectBoard(self, img):
        rows, cols, _ = img.shape
        virtual_board = np.zeros((rows, cols, 3), dtype=np.uint8)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        board_contour = max(contours, key=cv2.contourArea)
        
        cv2.drawContours(img, [board_contour], -1, (0, 255, 0), 2)
        # cv2.drawContours(virtual_board, [board_contour], -1, (0, 255, 0), 2)
        
        (board_x, board_y, board_w, board_h) = cv2.boundingRect(board_contour)
        
        # create cells
        board_w -= 397
        board_x += 397
        board_y += 5
        
        block_width = int(board_w / 12)
        block_height = int(board_h / 22)
        
        
        # detect pieces
        tetro = {
            "j": [248, 155, 99],
            "l": [87, 197, 84],
            "o": [153, 153, 153],
            "i": [27, 55, 237],
            "s": [53,180,241],
            "t": [194, 82, 197],
            "z": [33, 116, 238]
        }
        
        for key in tetro:
            color = tetro[key]
            color = np.array(color)

            mask = cv2.inRange(img, np.add(color, -1), np.add(color, 1))
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(virtual_board, (x, y), (x + w, y + h), (100, 0, 0), 2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (100, 0, 0), 2)

                for n in range(22):
                    for n2 in range(12):
                        block_x = n2 * block_width
                        block_y = n * block_height


                        # cv2.rectangle(virtual_board, (block_x + board_x, block_y + board_y), (block_x + block_width + board_x, block_y + block_height + board_y), (0, 0, 0), 1)
                        cv2.rectangle(img, (block_x + board_x, block_y + board_y), (block_x + block_width + board_x, block_y + block_height + board_y), (0, 0, 0), 1)
                        
                        if board_x + block_x < x < board_x + block_x + block_width and board_y + block_y < y < board_y + block_y + block_height:
                            self.board[n][n2] = 1
        
        
        print(self.board)
        
    def getNextState(self):
        state = {}
        
        n_rot = 0
        
        if self.piece_id == "z" or self.piece_id == "s" or self.piece_id == "j":
            n_rot = 2
        elif self.piece_id == "i":
            n_rot = 1
        elif self.piece_id == "l":
            n_rot = 3
        else:
            n_rot = 3
        return state
    
        
    def getScore(self):
        img_data = pytesseract.image_to_string(Image.fromarray(self.board))
        
        
