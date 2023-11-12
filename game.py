import player
import cv2
import numpy as np
from PIL import ImageGrab
import pywinctl as pwc
import time
import subprocess
# import pytesserac
import torch
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By


class Game:
    
    def __init__(self):
        print("Game started")
        self.Player = player.Player("Les Hackathon")
        self.board = np.zeros((22, 12))
        self.piece_id = 0
        self.piece = [[0,0,0],[0,0,0],[0,0,0]]
        self.score = 0
        self.holes = 0
        self.gameover = False
        self.img = 0
        self.tetrominoes = 0
        self.cleared_lines = 0
    
    def reset(self):
        self.board = np.zeros((22, 12))
        self.piece_id = 0
        self.score = 0
        self.holes = 0
        self.gameover = False
        self.tetrominoes = 0
        self.cleared_lines = 0
        self.piece = [[0,0,0],[0,0,0],[0,0,0]]
        self.img = 0
        
        
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
            "i": [[0,0,0],[1,1,1],[0,0,0]],
            "t": [[0,1,0],[1,1,1],[0,0,0]]
        }
        
        for key, value in all_piece.items():
            if (piece == value).all():
                self.piece_id = key
                self.piece = value
        
        # replace 2 upper line of matrix with 0
        for i in range(12):
            self.board[0][i] = 0
        for i in range(12):
            self.board[1][i] = 0
            
    def detectBoard(self, img):
        self.img = img
        self.board = np.zeros((22, 12))
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
        
    def check_collision(self, piece, pos):
        future_y = pos["y"] + 1
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if future_y + y > 21 or self.board[future_y + y][pos["x"] + x] and piece[y][x]:
                    return True
        return False

    def getNextState(self):
        def putOnMatrix(piece, pos):
            board = np.array(self.board)
            for y in range(len(piece)):
                for x in range(len(piece[y])):
                    if piece[y][x]:
                        board[pos["y"] + y][pos["x"] + x] = 1
            return board
        def getMaxLenOfForm(form):
            max_size = 0
            for i in range(3):
                count = 0
                for j in range(3):
                    if(form[i][j] == 1):
                        count+=1
                max_size = max(max_size, count)
            return max_size
            
        n_rot = 4
        if(self.piece_id == "i"):
            n_rot = 1
        elif(self.piece_id == "s" or self.piece_id == "z"):
            n_rot = 2
        
        states = {}
        board = np.array(self.board)
        curr_piece = np.array(self.piece)
        for i in range(n_rot):
            # size of piece
            valid_xs = 12 - getMaxLenOfForm(curr_piece)
            for x in range(valid_xs):
                pos = {"x": x, "y": 0}
                while not self.check_collision(curr_piece, pos):
                    pos["y"] += 1
                board = putOnMatrix(curr_piece, {"x": pos["x"], "y": pos["y"]})
                states[(x, i)] = self.getStateProp(board)
                print(board)
            curr_piece = np.rot90(curr_piece, 1)
        exit(0)
        return states
    
    def getHoles(self, board):
        
        num_holes = 0
        for col in zip(*board):
            row = 2
            while row < 22 and col[row] == 0:
                row += 1
            num_holes += len([x for x in col[row + 1:] if x == 0])
        print("holes: ",num_holes)
        return num_holes

    def getBumpAndHeight(self):
        board = np.array(self.board)
        mask = board != 0
        invert_heights = np.where(mask.any(axis=0), np.argmax(mask, axis=0), 22)
        h = 22 - invert_heights
        total_height = np.sum(h)
        currs = h[:-1]
        next = h[1:]
        diff = np.abs(currs - next)
        bumpiness = np.sum(diff)
        print("bumpiness: ",bumpiness)
        print("height: ",total_height)
        return bumpiness, total_height
    
    def getStateProp(self, board):
        def nbrOfFullLines(board):
            lines = 0
            for i in range(22):
                if np.all(board[i] == 1):
                    lines += 1
            return lines
        
        bump, height = self.getBumpAndHeight()
        holes = self.getHoles(board)
        full_line = nbrOfFullLines(board)
        
        return torch.FloatTensor([full_line, holes, bump, height])
    
    def checkGameOver(self):
        template = cv2.imread("lose.png")
        res = cv2.matchTemplate(self.img, template, cv2.TM_CCOEFF_NORMED)
        if np.max(res) > 0.9:
            print("Game Over")
            return True
        else:
            return False
    
    def step(self, action):
        def putOnMatrix(piece, pos):
            board = np.array(self.board)
            for y in range(len(piece)):
                for x in range(len(piece[y])):
                    if piece[y][x]:
                        board[pos["y"] + y][pos["x"] + x] = 1
            return board
        
        def nbrOfFullLines(board):
            lines = 0
            for i in range(22):
                if np.all(board[i] == 1):
                    lines += 1
            return lines
        f_pos, rot = action
        pos = {"x": 6, "y": 0}
        for _ in range(rot):
            self.Player.up()
            self.piece = np.rot90(self.piece)
            
        while f_pos != pos["x"]:
            if pos["x"] < f_pos:
                self.Player.right()
                pos["x"] += 1
            else:
                self.Player.left()
                pos["x"] -= 1
        
        for _ in range(12):
            self.Player.down()
        
        while not self.check_collision(self.piece, pos):
            pos["y"] += 1
        
        board = putOnMatrix(self.piece, {"x": pos["x"], "y": pos["y"]})
        # print(board)
        
        full_lines = nbrOfFullLines(board)
        
        self.score += (1 + (full_lines ** 2) * 12)
        self.cleared_lines += full_lines
        self.tetrominoes += 1
        
        if(self.checkGameOver()):
            self.score -= 2
            self.gameover = True
        
        return self.score, self.gameover

        
        