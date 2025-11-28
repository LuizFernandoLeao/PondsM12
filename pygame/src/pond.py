import pygame
import sys
import random
import serial
import time
from utils.loader import load_image


SERIAL_PORT = 'COM6' 
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"Conectado ao Pico na porta {SERIAL_PORT}")
    ser.flush()
except serial.SerialException:
    print("ERRO DE SERIAL: O jogo vai rodar, mas sem o Pico.")
    ser = None

pygame.init()

WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Detecção de Colisão com Pico W")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = load_image("python.png")
        self.current_size = 128
        self.image = pygame.transform.scale(self.original_image, (self.current_size, self.current_size))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
    
    def update_size(self, new_size):
        if abs(new_size - self.current_size) > 3: 
            self.current_size = new_size
            center_backup = self.rect.center
            self.image = pygame.transform.scale(self.original_image, (self.current_size, self.current_size))
            self.rect = self.image.get_rect()
            self.rect.center = center_backup

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: self.rect.y += self.speed
        
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("star.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

player = Player()
obstacles = pygame.sprite.Group()
MAX_ENEMY = 10

for _ in range(MAX_ENEMY):
    x = random.randint(50, WIDTH - 150)
    y = random.randint(50, HEIGHT - 150)
    obstacles.add(Obstacle(x, y))

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(obstacles)

clock = pygame.time.Clock()
running = True
score = 0
game_won = False
font = pygame.font.Font(None, 36)

while running:
    if ser and ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line.startswith("SIZE:"):
                size_str = line.split(":")[1]
                player.update_size(int(size_str))
        except:
            pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)
    
    if not game_won:
        hits = pygame.sprite.spritecollide(player, obstacles, True)
        score += len(hits)
        if score == MAX_ENEMY:
            game_won = True
            if ser:
                ser.write(b"WIN\n")
    
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    if game_won:
        text = font.render(f"VITÓRIA! Score: {score}", True, GREEN)
        screen.blit(text, (WIDTH//2 - 100, HEIGHT//2))
    else:
        text = font.render(f"Pontuação: {score}/{MAX_ENEMY}", True, RED)
        screen.blit(text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)


if ser:
    print("Enviando comando para desligar LED...")
    ser.write(b"OFF\n") 
    time.sleep(0.1)
    ser.close()

pygame.quit()
sys.exit()