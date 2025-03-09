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

# Game settings
difficulty_levels = {
    "Easy": (1, 10),
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

# Show difficulty selection
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

def main():
    mode = show_menu()
    zombie_speed, zombie_count = difficulty_levels[mode]
    
    tank_x, tank_y = WIDTH // 2, HEIGHT - 60
    bullets = []
    score = 0
    start_time = time.time()
    font = pygame.font.Font(None, 36)
    zombies = [
        {"rect": pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT // 2), 50, 50), 
         "speed": random.uniform(1, zombie_speed), 
         "type": random.choice(["zombie1", "zombie2", "zombie3"])} 
        for _ in range(zombie_count)
    ]
    obstacles = [Obstacle(random.randint(50, WIDTH - 100), random.randint(100, HEIGHT - 200), 50, 20, True) for _ in range(5)]
    running = True

    while running:
        screen.fill(BLACK)
        if assets["background"]:
            screen.blit(assets["background"], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tank_x = max(0, tank_x - 10)
                if event.key == pygame.K_RIGHT:
                    tank_x = min(WIDTH - 50, tank_x + 10)
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullets.append({"x": tank_x + 25, "y": tank_y, "angle": math.atan2(pygame.mouse.get_pos()[1] - tank_y, pygame.mouse.get_pos()[0] - tank_x)})
                if assets["gunshot"]:
                    assets["gunshot"].play()

        for bullet in bullets[:]:
            bullet["x"] += 10 * math.cos(bullet["angle"])
            bullet["y"] += 10 * math.sin(bullet["angle"])
            pygame.draw.circle(screen, RED, (int(bullet["x"]), int(bullet["y"])), 5)
            if bullet["x"] < 0 or bullet["x"] > WIDTH or bullet["y"] < 0 or bullet["y"] > HEIGHT:
                bullets.remove(bullet)

        for zombie in zombies[:]:
            zombie['rect'].y += zombie['speed']
            screen.blit(assets[zombie['type']], zombie['rect'])
            for bullet in bullets[:]:
                if zombie['rect'].collidepoint(bullet['x'], bullet['y']):
                    score += 1
                    bullets.remove(bullet)
                    zombies.remove(zombie)

        for obstacle in obstacles:
            obstacle.move()
            obstacle.draw()
        
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(assets["tank"], (tank_x, tank_y))
        pygame.display.flip()
        pygame.time.delay(30)

if __name__ == "__main__":
    main()