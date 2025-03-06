import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Initialize the Pygame mixer for sound
pygame.mixer.init()

# Define constants
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BUTTON_COLOR = (0, 0, 255)  # Blue button color
BUTTON_HOVER_COLOR = (0, 100, 255)  # Lighter blue for hover effect

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooting Gallery")

# Load images
try:
    zombie_image = pygame.image.load("zombie.jpg")  # Changed to zombie.jpg
    background_image = pygame.image.load("zombies.jpg")  # Changed background to zombies.jpg
    arrow_image = pygame.image.load("arrow.png")  # Load arrow image
except pygame.error as e:
    print("Error loading image: ", e)

# Scale images if needed (optional)
zombie_image = pygame.transform.scale(zombie_image, (50, 50))  # Resize the zombie image to 50x50
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Resize background to screen size
arrow_image = pygame.transform.scale(arrow_image, (30, 30))  # Resize arrow image

# Load the sound effect
try:
    hit_sound = pygame.mixer.Sound("sound.mp3")  # Load your MP3 file
except pygame.error as e:
    print("Error loading sound: ", e)

# Define game variables
zombies = []
num_zombies = 8  # Total number of zombies (targets)
time_limit = 30000  # 30 seconds limit
score = 0
start_ticks = 0  # Start time for the timer (initialized after game starts)

# Set up the timer and score
zombie_speed = 3  # Speed of zombies movement
paused = False  # Pause state

# Main Menu Drawing Function
def draw_main_menu():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 48)
    
    title_text = font.render("Zombie Shooting Gallery", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

    # Start Game Button
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if start_button.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, start_button)  # Highlight button on hover
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, start_button)
    start_text = font.render("Start Game", True, WHITE)
    screen.blit(start_text, (start_button.x + start_button.width // 2 - start_text.get_width() // 2, start_button.y + start_button.height // 4))

    # Quit Game Button
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)
    if quit_button.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, quit_button)  # Highlight button on hover
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, quit_button)
    quit_text = font.render("Quit Game", True, WHITE)
    screen.blit(quit_text, (quit_button.x + quit_button.width // 2 - quit_text.get_width() // 2, quit_button.y + quit_button.height // 4))

    pygame.display.flip()

    return start_button, quit_button

# Calculate the angle between the arrow and the zombie
def get_angle_to_zombie(arrow_pos, zombie_pos):
    dx = zombie_pos[0] - arrow_pos[0]
    dy = zombie_pos[1] - arrow_pos[1]
    angle = math.atan2(dy, dx)
    return angle

# Game Loop Function
def game_loop():
    global score, zombies, start_ticks, paused

    # Reset the game variables for a new game
    score = 0
    zombies = [pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 50, 50) for _ in range(num_zombies)]
    start_ticks = pygame.time.get_ticks()  # Start the timer

    running = True
    while running:
        # Draw the background image
        screen.blit(background_image, (0, 0))  # Draw the new background (zombies.jpg) at the top-left corner

        if paused:
            font = pygame.font.Font(None, 48)
            pause_text = font.render("Paused", True, BLACK)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3))
        else:
            # Check time limit
            elapsed_time = pygame.time.get_ticks() - start_ticks
            remaining_time = (time_limit - elapsed_time) / 1000  # Remaining time in seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check for a collision with any zombie
                    for zombie in zombies:
                        if zombie.collidepoint(event.pos):
                            score += 1
                            zombie.x = random.randint(50, WIDTH - 50)  # Move zombie to a new random position after being hit
                            zombie.y = random.randint(50, HEIGHT - 50)
                            hit_sound.play()  # Play the sound when the zombie is hit

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Pause when the 'P' key is pressed
                        paused = not paused  # Toggle pause state

            # Get the position of the mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Draw the arrow and point it towards the closest zombie
            closest_zombie = min(zombies, key=lambda z: math.hypot(z.centerx - mouse_x, z.centery - mouse_y))
            arrow_angle = get_angle_to_zombie((mouse_x, mouse_y), closest_zombie.center)

            # Rotate the arrow image to point in the right direction
            rotated_arrow = pygame.transform.rotate(arrow_image, math.degrees(arrow_angle))
            arrow_rect = rotated_arrow.get_rect(center=(mouse_x, mouse_y))

            screen.blit(rotated_arrow, arrow_rect)  # Draw the rotated arrow at the mouse position

            # Draw the zombies
            for zombie in zombies:
                screen.blit(zombie_image, zombie)  # Use the zombie's rect to position the image

            # Display score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            # Display remaining time
            time_text = font.render(f"Time Left: {int(remaining_time)}s", True, BLACK)
            screen.blit(time_text, (WIDTH - 150, 10))

            # Check if the time limit has been reached
            if elapsed_time > time_limit:
                # Time's up, display game over screen
                game_over_text = font.render("Game Over!", True, BLACK)
                final_score_text = font.render(f"Final Score: {score}", True, BLACK)
                screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
                screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))

                pygame.display.flip()
                pygame.time.delay(2000)  # Show game over for 2 seconds
                running = False  # End the game

        pygame.display.flip()
        pygame.time.delay(30)

    pygame.quit()

# Main Function
def main():
    running = True
    while running:
        start_button, quit_button = draw_main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_loop()  # Start the game
                elif quit_button.collidepoint(event.pos):
                    running = False  # Quit the game

    pygame.quit()

if __name__ == "__main__":
    main()
