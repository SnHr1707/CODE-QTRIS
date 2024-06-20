import numpy as np
import pygame

# Define Tetromino shapes
SHAPES = [
    np.array([[1, 1, 1, 1]]),  # I
    np.array([[1, 1, 1], [0, 1, 0]]),  # T
    np.array([[1, 1], [1, 1]]),  # O
    np.array([[0, 1, 1], [1, 1, 0]]),  # S
    np.array([[1, 1, 0], [0, 1, 1]]),  # Z
    np.array([[1, 1, 1], [1, 0, 0]]),  # L
    np.array([[1, 1, 1], [0, 0, 1]])   # J
]
#All Constants
TILE_SIZE = 20


#Cell height = 15
#Added height variable to uh yeah u know(If you don't it's for the line below the QR Code)
class Tetromino:
    def __init__(self, shape, x, y):
        self.shape = shape
        self.x = x
        self.y = y
        self.update_height()
    
    def update_height(self):
        self.height = self.shape.shape[0] * 15 
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = np.rot90(self.shape)
        self.update_height()

    def draw(self, surface, color=(255, 255, 255)):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, color, (self.x + x * TILE_SIZE, self.y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Draw grid
def draw_grid(screen, width, height):
    for i in range(width):
        for j in range(height):
            pygame.draw.rect(screen, 'black', (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)