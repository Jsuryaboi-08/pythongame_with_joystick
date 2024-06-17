import pygame
import serial

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the title of the window
pygame.display.set_caption("Ball Breaker")

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the fonts
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)

# Set up the ball
ball_x = screen_width / 2
ball_y = screen_height / 2
ball_speed_x = 5
ball_speed_y = 5
ball_radius = 10

# Set up the disc
disc_width = 100
disc_height = 20
disc_x = screen_width / 2 - disc_width / 2  # Center the disc horizontally

# Set up the serial connection
ser = serial.Serial('COM9', 9600)  # Replace 'COM9' with your Arduino's serial port

# Create clock outside the game loop
clock = pygame.time.Clock()

# Set up the points system
points = 0
game_over = False

def show_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def reset_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, points, game_over
    ball_x = screen_width / 2
    ball_y = screen_height / 2
    ball_speed_x = 5
    ball_speed_y = 5
    points = 0
    game_over = False

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:
        # Read input from joystick
        try:
            y_value = int(ser.readline().decode().strip())
            # Scale the y_value to fit within the screen height
            disc_y = screen_height - disc_height - (y_value / 1023.0) * (screen_height - disc_height)
        except ValueError:
            continue

        # Move the ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Bounce the ball off the walls
        if ball_x <= 0 or ball_x + ball_radius >= screen_width:
            ball_speed_x = -ball_speed_x
        if ball_y <= 0:
            ball_speed_y = -ball_speed_y
        if ball_y + ball_radius >= screen_height:
            # Game over
            game_over = True

        # Bounce the ball off the disc
        if ball_y + ball_radius >= disc_y and disc_x <= ball_x <= disc_x + disc_width:
            ball_speed_y = -ball_speed_y
            points += 1

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)
    pygame.draw.rect(screen, WHITE, (int(disc_x), int(disc_y), disc_width, disc_height))
    show_text(f'Points: {points}', small_font, WHITE, screen, screen_width / 2, 30)

    if game_over:
        show_text('Game Over!', font, WHITE, screen, screen_width / 2, screen_height / 2)
        show_text('Press R to Restart', small_font, WHITE, screen, screen_width / 2, screen_height / 2 + 60)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
