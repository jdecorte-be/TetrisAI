import player
import shape
import cv2
import numpy as np

class Game:
    
    def __init__(self):
        print("Game started")
        self.Player = player.Player
        self.img = cv2.imread("screen2.png")
        self.board = np.zeros((22, 12))
        
    
    def detectBoard(self):
        rows, cols, _ = self.img.shape
        virtual_board = np.zeros((rows, cols, 3), dtype=np.uint8)
        
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        contours_detected = False
        
        while not contours_detected:
            # take screenshot
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                contours_detected = True
                
            board_contour = max(contours, key=cv2.contourArea)
            
            cv2.drawContours(self.img, [board_contour], -1, (0, 255, 0), 2)
            cv2.drawContours(virtual_board, [board_contour], -1, (0, 255, 0), 2)
            
            (board_x, board_y, board_w, board_h) = cv2.boundingRect(board_contour)
            
            # create cells
            board_w -= 525
            board_x += 525
            
            block_width = int(board_w / 12)
            block_height = int(board_h / 22)
            
            
            # detect pieces
            tetro = {
                "j": [250, 164, 51],
                "i": [0, 0, 255],
                # "o": [],
                "l": [80, 196, 56],
                "s": [28,173,255],
                # "t": [],
                "z": [0, 102, 255]
            }
            
            for key in tetro:
                color = tetro[key]
                color = np.array(color)

                mask = cv2.inRange(self.img, np.add(color, -30), color)
                
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    cv2.rectangle(virtual_board, (x, y), (x + w, y + h), (100, 0, 0), 2)

                    for n in range(22):
                        for n2 in range(12):
                            block_x = n2 * block_width
                            block_y = n * block_height


                            cv2.rectangle(virtual_board, (block_x + board_x, block_y + board_y), (block_x + block_width + board_x, block_y + block_height + board_y), (255, 255, 255), 1)
                            
                            if board_x + block_x <= x < board_x + block_x + block_width and board_y + block_y <= y < board_y + block_y + block_height:
                                self.board[n][n2] = 1
            
            
        # show result
        # cv2.imshow('Board Edge', self.img)
        print(self.board)
        cv2.imshow('Board Edge', virtual_board)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def getFirstPieces():
        
        pass
        
    def startNewGame():
        pass

