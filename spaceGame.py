import pygame
import random
import sys
import os

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Shuttle Shooting Game")   

# Colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS
clock = pygame.time.Clock()
FPS = 90

# Load shuttle image
try:
    shuttle_img = pygame.image.load("shuttle.png").convert_alpha()
    shuttle_img = pygame.transform.scale(shuttle_img, (60, 60))
except:
    print("⚠️ Couldn't load 'shuttle.png'. Please place it in the same folder.")
    sys.exit()

# Bullet
bullet_img = pygame.Surface((5, 20))
bullet_img.fill((0, 255, 0))

# ------------------- Classes -----------------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = shuttle_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 6

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = random.randint(15, 40)
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.color = [random.randint(50, 255) for _ in range(3)]
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -40)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -40)
        self.speed = random.randint(2, 5)

# ------------------- Game Setup -----------------------

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for _ in range(6):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

score = 0
font = pygame.font.SysFont("Arial", 30)

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# ------------------- Game Loop -----------------------

running = True
while running:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shoot bullet
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Update
    all_sprites.update()

    # Collision: bullet hits enemy
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        score += 10
        new_enemy = Enemy()
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)

    # Collision: enemy hits player
    if pygame.sprite.spritecollideany(player, enemies, pygame.sprite.collide_circle):
        draw_text(screen, "GAME OVER", 64, WIDTH//2 - 160, HEIGHT//2)
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, f"Score: {score}", 28, 10, 10)
    pygame.display.flip()

pygame.quit()