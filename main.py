import pygame
import sys
from qtromino import Tetromino, SHAPES
from qr_code import generate_qr_code
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 800
BG_COLOR = (0, 0, 0)
FPS = 60

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CODE QTRIS')

# Generate and load QR code
generate_qr_code('https://example.com')
qr_code_img = pygame.image.load("assets/qr_code.png")

# Resize QR code to fit within the screen dimensions
qr_code_width, qr_code_height = qr_code_img.get_size()
scale_factor = min(WIDTH / qr_code_width, HEIGHT / qr_code_height)
new_size = (int(qr_code_width * scale_factor), int(qr_code_height * scale_factor))
qr_code_img = pygame.transform.scale(qr_code_img, new_size)

# Position the QR code in the middle, slightly lower
qr_code_x = (WIDTH - new_size[0]) // 2
qr_code_y = (HEIGHT - new_size[1]) // 2 + 50  # Adjust the +50 value as needed to position it lower

#The bottom of the QR Code
qr_code_bottom_y = qr_code_y + new_size[1] - 60 #idk why but can't figure out the 60

# Create Tetromino
current_tetromino = Tetromino(random.choice(SHAPES), WIDTH // 2, 0)

BASE_MOVE_SPEED = 15  # Pixels per second
BOOSTED_MOVE_SPEED = 15  # Pixels per second when down arrow is pressed
MOVE_DELAY = 1000  # milliseconds

# Variables for continuous movement
move_left = False
move_right = False
move_down = False
move_timer = 0

#Randomly selects Shape
def create_new_tetromino():
    return Tetromino(random.choice(SHAPES), WIDTH // 2, 0)

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    current_time = pygame.time.get_ticks()
    dt = current_time - move_timer  # Calculate time since last movement
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_DOWN:
                move_down = True
            elif event.key == pygame.K_UP:
                current_tetromino.rotate()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_DOWN:
                move_down = False

    # Automatic downward movement
    if current_time - move_timer > MOVE_DELAY:
        current_tetromino.move(0, BASE_MOVE_SPEED * (MOVE_DELAY / 1000))  # Move based on MOVE_DELAY
        move_timer = current_time

    # Boosted downward movement when down arrow key is pressed
    if move_down:
        current_tetromino.move(0, BASE_MOVE_SPEED * (MOVE_DELAY / 1000))
    
    #Normal left and right movement
    elif move_left:
        current_tetromino.move(-BASE_MOVE_SPEED * (MOVE_DELAY / 1000), 0)
        
    elif move_right:
        current_tetromino.move(BASE_MOVE_SPEED * (dt / 1000), 0)

    # Check if Tetromino has reached the bottom line of QR code
    if current_tetromino.y + current_tetromino.height > qr_code_bottom_y:
        # Create a new Tetromino with a random shape
        current_tetromino = create_new_tetromino()

    # Limit Tetromino position not to go below the QR code
    if current_tetromino.y + current_tetromino.height > qr_code_bottom_y:
        current_tetromino.y = qr_code_bottom_y - current_tetromino.height
        
    # Clear screen
    screen.fill(BG_COLOR)
    
    # Draw QR code background
    screen.blit(qr_code_img, (qr_code_x, qr_code_y))

    # Draw current Tetromino
    current_tetromino.draw(screen)

    # Refresh screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
