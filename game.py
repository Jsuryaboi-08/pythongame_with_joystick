import pygame
import serial
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle dimensions
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90

# Ball dimensions
BALL_WIDTH = 20
BALL_HEIGHT = 20

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Initialize clock
clock = pygame.time.Clock()

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move(self, y):
        self.rect.y += y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Ball class
class Ball:
    def __init__(self, x, y, x_vel, y_vel):
        self.rect = pygame.Rect(x, y, BALL_WIDTH, BALL_HEIGHT)
        self.x_vel = x_vel
        self.y_vel = y_vel

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.y_vel *= -1
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.x_vel *= -1

# Initialize paddles and ball
player_paddle = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ai_paddle = Paddle(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball(SCREEN_WIDTH // 2 - BALL_WIDTH // 2, SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2, 5, 5)            

# Setup serial communication
ser = serial.Serial('COM3', 115200)  # Replace 'COM3' with your ESP32 serial port

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read data from serial
    try:
        data = ser.readline().decode('utf-8').strip()
        xValue, buttonState = map(int, data.split(','))
        yMove = (xValue - 2048) // 128  # Adjust the divisor to control paddle speed
    except:
        yMove = 0

    # Update paddle position
    player_paddle.move(yMove)