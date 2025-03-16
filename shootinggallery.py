import pygame
import random
import math
import os
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Zombie Shooting Gallery")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load assets
assets = {}
asset_files = {
    "tank": "tank.jpg",
    "zombie1": "zombie1.jpeg",
    "zombie2": "zombie2.jpeg",
    "zombie3": "zombie3.jpeg",
    "background": "zombies.jpg",
    "gunshot": "gunshot.mp3"
}

for key, file in asset_files.items():
    if os.path.exists(file):
        try:
            if file.endswith(".mp3"):
                assets[key] = pygame.mixer.Sound(file)
            else:
                assets[key] = pygame.image.load(file)
        except pygame.error as e:
            print(f"Error loading {file}: {e}")
            assets[key] = None
    else:
        print(f"Warning: {file} not found!")
        assets[key] = None

# Scale images
if assets["tank"]:
    assets["tank"] = pygame.transform.scale(assets["tank"], (50, 50))
for key in ["zombie1", "zombie2", "zombie3"]:
    if assets.get(key):
        assets[key] = pygame.transform.scale(assets[key], (50, 50))
if assets["background"]:
    assets["background"] = pygame.transform.scale(assets["background"], (WIDTH, HEIGHT))

# Game settings for difficulty levels
difficulty_levels = {
    "Easy": (1, 10),    # Starting speed, count of zombies
    "Medium": (2, 15),
    "Hard": (3, 20)
}

# Obstacle class
class Obstacle:
    def __init__(self, x, y, width, height, moving=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.moving = moving
        self.direction = 1 if moving else 0
    
    def move(self):
        if self.moving:
            self.rect.x += self.direction * 3
            if self.rect.x <= 50 or self.rect.x >= WIDTH - 50:
                self.direction *= -1
    
    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# Show difficulty selection menu
def show_menu():
    font = pygame.font.Font(None, 50)
    selected = 0
    difficulties = list(difficulty_levels.keys())

    while True:
        screen.fill(BLACK)
        title = font.render("Select Difficulty", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        for i, difficulty in enumerate(difficulties):
            color = RED if i == selected else WHITE
            text = font.render(difficulty, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(difficulties)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(difficulties)
                if event.key == pygame.K_RETURN:
                    return difficulties[selected]

# Create button for pause and restart
def draw_button(x, y, width, height, text, color, text_color):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, (x + width // 2 - text_surface.get_width() // 2, y + height // 2 - text_surface.get_height() // 2))

def check_button_click(x, y, width, height, mouse_pos):
    return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

# Function to restart the game
def restart_game():
    return True  # Simply return True to restart the game

# Main game loop
def main():
    mode = show_menu()  # Get the selected difficulty
    zombie_speed, zombie_count = difficulty_levels[mode]
    
    # Initial tank setup
    tank_x, tank_y = WIDTH // 2, HEIGHT - 60
    bullets = []
    score = 0
    level = 1
    start_time = time.time()
    font = pygame.font.Font(None, 36)

    # Function to generate zombies
    def generate_zombies(level):
        level_multiplier = 1 + (level - 1) * 0.5  # Increase difficulty each level
        return [
            {"rect": pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT // 2), 50, 50), 
             "speed": random.uniform(1, zombie_speed * level_multiplier), 
             "type": random.choice(["zombie1", "zombie2", "zombie3"])} 
            for _ in range(int(zombie_count * level_multiplier))
        ]

    # Initial zombie generation
    zombies = generate_zombies(level)

    # Obstacles that move on the screen
    obstacles = [Obstacle(random.randint(50, WIDTH - 100), random.randint(100, HEIGHT - 200), 50, 20, True) for _ in range(5)]

    running = True
    paused = False  # Track whether the game is paused

    while running:
        screen.fill(BLACK)
        if assets["background"]:
            screen.blit(assets["background"], (0, 0))

        # Handle events (quitting, shooting, moving)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if paused:
                    # Check if the pause menu buttons are clicked
                    if check_button_click(WIDTH - 120, 10, 100, 50, pygame.mouse.get_pos()):
                        paused = not paused  # Toggle pause
                    elif check_button_click(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, pygame.mouse.get_pos()):
                        return restart_game()  # Restart the game when clicked
                else:
                    # In the gameplay state, target zombies when clicked
                    for zombie in zombies[:]:
                        if zombie['rect'].collidepoint(pygame.mouse.get_pos()):
                            zombies.remove(zombie)
                            score += 1
                            break  # Stop checking after one zombie is hit
                    bullets.append({"x": tank_x + 25, "y": tank_y, "angle": math.atan2(pygame.mouse.get_pos()[1] - tank_y, pygame.mouse.get_pos()[0] - tank_x)})
                    if assets["gunshot"]:
                        assets["gunshot"].play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tank_x = max(0, tank_x - 10)
                if event.key == pygame.K_RIGHT:
                    tank_x = min(WIDTH - 50, tank_x + 10)
                if event.key == pygame.K_RETURN and paused:  # Press Enter to resume the game
                    paused = False

        if paused:
            paused_text = font.render("PAUSED - Press Enter to Resume", True, WHITE)
            screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2 - 50))
            pygame.display.flip()
            continue  # Skip the rest of the game loop while paused

        # Move bullets and check for collision with zombies
        for bullet in bullets[:]:
            bullet["x"] += 10 * math.cos(bullet["angle"])
            bullet["y"] += 10 * math.sin(bullet["angle"])
            pygame.draw.circle(screen, RED, (int(bullet["x"]), int(bullet["y"])), 5)
            if bullet["x"] < 0 or bullet["x"] > WIDTH or bullet["y"] < 0 or bullet["y"] > HEIGHT:
                bullets.remove(bullet)

        # Update zombies and check for collisions
        for zombie in zombies[:]:
            zombie['rect'].y += zombie['speed']
            screen.blit(assets[zombie['type']], zombie['rect'])
            # Check if any bullet collides with a zombie
            for bullet in bullets[:]:
                if zombie['rect'].collidepoint(bullet["x"], bullet["y"]):
                    zombies.remove(zombie)
                    bullets.remove(bullet)
                    score += 1
                    break  # Stop checking after a zombie is hit

        # Move and draw obstacles
        for obstacle in obstacles:
            obstacle.move()
            obstacle.draw()

        # Display the difficulty level text in the center of the screen
        difficulty_text = font.render(f"Difficulty: {mode}", True, WHITE)
        screen.blit(difficulty_text, (WIDTH // 2 - difficulty_text.get_width() // 2, 20))

        # Level progression check (if all zombies are defeated)
        if len(zombies) == 0:
            if level < 3:  # Check if we reached Level 3
                level += 1
                zombies = generate_zombies(level)
            else:
                screen.fill(BLACK)
                game_over_text = font.render("You Win! Game Over!", True, WHITE)
                screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.delay(3000)
                return restart_game()  # Restart the game after winning

        # Display score and level
        screen.blit(font.render(f"Score: {score}   Level: {level}", True, WHITE), (10, 10))
        screen.blit(assets["tank"], (tank_x, tank_y))

        # Draw pause button at the top-right corner
        draw_button(WIDTH - 120, 10, 100, 50, "Pause", GREEN, WHITE)

        # Draw restart button when the game is over
        if paused or len(zombies) == 0:
            draw_button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, "Restart", GREEN, WHITE)

        pygame.display.flip()

        pygame.time.delay(30)  # Slight delay between frames to make the game playable

# Handle KeyboardInterrupt gracefully
if __name__ == "__main__":
    try:
        while True:  # Loop the game to allow restarting
            main()
    except KeyboardInterrupt:
        pygame.quit()
        print("Game interrupted, quitting gracefully...")
        exit()
