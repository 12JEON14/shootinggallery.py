import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Initialize the Pygame mixer for sound
pygame.mixer.init()

# Define constants
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Gallery")

# Load images
try:
    duck_image = pygame.image.load("duck.png")  # Replace with your duck image path
    background_image = pygame.image.load("background_image.jpg")  # Replace with your background image path
except pygame.error as e:
    print("Error loading image: ", e)

# Scale images if needed (optional)
duck_image = pygame.transform.scale(duck_image, (50, 50))  # Resize the duck image to 50x50
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Resize background to screen size

# Load the sound effect
try:
    hit_sound = pygame.mixer.Sound("sound.mp3")  # Load your MP3 file
except pygame.error as e:
    print("Error loading sound: ", e)

# Define game variables
ducks = []
num_ducks = 8  # Total number of ducks (targets)
time_limit = 30000  # 30 seconds limit
score = 0
start_ticks = 0  # Start time for the timer (initialized after game starts)

# Set up the timer and score
duck_speed = 3  # Speed of ducks movement
paused = False  # Pause state

def draw_main_menu():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 48)
    
    title_text = font.render("Shooting Gallery", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

    # Start Game Button
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    pygame.draw.rect(screen, RED, start_button)
    start_text = font.render("Start Game", True, WHITE)
    screen.blit(start_text, (start_button.x + start_button.width // 2 - start_text.get_width() // 2, start_button.y + start_button.height // 4))

    # Quit Game Button
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)
    pygame.draw.rect(screen, RED, quit_button)
    quit_text = font.render("Quit Game", True, WHITE)
    screen.blit(quit_text, (quit_button.x + quit_button.width // 2 - quit_text.get_width() // 2, quit_button.y + quit_button.height // 4))

    pygame.display.flip()

    return start_button, quit_button

def game_loop():
    global score, ducks, start_ticks, duck_speed, paused

    # Reset the game variables for a new game
    score = 0
    ducks = [pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 50, 50) for _ in range(num_ducks)]
    start_ticks = pygame.time.get_ticks()  # Start the timer

    running = True
    while running:
        # Draw the background image
        screen.blit(background_image, (0, 0))  # Draw the background at the top-left corner

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
                    # Check for a collision with any duck
                    for duck in ducks:
                        if duck.collidepoint(event.pos):
                            score += 1
                            duck.x = random.randint(50, WIDTH - 50)
                            duck.y = random.randint(50, HEIGHT - 50)
                            hit_sound.play()  # Play the sound when the duck is hit

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Pause when the 'P' key is pressed
                        paused = not paused  # Toggle pause state

            # Move the ducks randomly and bounce them off the walls
            for duck in ducks:
                duck.x += random.choice([-1, 1]) * duck_speed
                duck.y += random.choice([-1, 1]) * duck_speed

                # Keep the duck within bounds and bounce off the edges
                if duck.left < 0 or duck.right > WIDTH:
                    duck_speed *= -1  # Reverse direction on x-axis
                if duck.top < 0 or duck.bottom > HEIGHT:
                    duck_speed *= -1  # Reverse direction on y-axis

                # Draw the duck image
                screen.blit(duck_image, duck)  # Use the duck's rect to position the image

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
