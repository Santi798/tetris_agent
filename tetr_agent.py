import numpy as np
import matplotlib.pyplot as plt
from utilities import Pieces

class Agent:
    def __init__(self):
        self.grid = np.zeros((20, 10))
        self.pieces = Pieces()
    
    def place_piece(self, piece, col, row):
        p_rows, p_cols = piece.shape
        self.grid[row:row+p_rows, col:col+p_cols] += piece

    def receive_perception(self, color):
        piece = self.pieces.get(color)
        self.place_piece(piece, 4, 0)

if __name__ == '__main__':
    agent = Agent()
    while True:
        color = input()
        agent.receive_perception(color)
        plt.imshow(agent.grid, cmap='gray')
        plt.show()