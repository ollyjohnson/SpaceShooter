import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 50
ASTEROID_WIDTH = 50
ASTEROID_HEIGHT = 50
BULLET_WIDTH = 5
BULLET_HEIGHT = 10

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
spaceship_img = pygame.Surface((SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
spaceship_img.fill(WHITE)

class Bullet:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,BULLET_WIDTH, BULLET_HEIGHT)

    def move(self):
        self.rect.y -= 5
    
    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)
 

class Asteroid:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0,SCREEN_WIDTH-ASTEROID_WIDTH), 0, ASTEROID_WIDTH, ASTEROID_HEIGHT)
        self.speed = random.randint(2,5)

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


def game():
    spaceship_x  = SCREEN_WIDTH // 2
    spaceship_y = SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10
    spaceship_speed = 5
    bullets = []
    asteroids = []
    asteroid_frequency = 2000
    asteroid_timer = 0

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and spaceship_x > 0:
            spaceship_x -= spaceship_speed
        if keys[pygame.K_RIGHT] and spaceship_x < SCREEN_WIDTH - SPACESHIP_WIDTH:
            spaceship_x += spaceship_speed
        if keys[pygame.K_SPACE]:
            bullets.append(Bullet(spaceship_x + SPACESHIP_WIDTH // 2 - BULLET_WIDTH // 2, spaceship_y))
        
        screen.fill(BLACK)
        screen.blit(spaceship_img, (spaceship_x, spaceship_y))

        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            if bullet.rect.y < 0:
                bullets.remove(bullet)
        
        current_time = pygame.time.get_ticks()
        if current_time - asteroid_timer > asteroid_frequency:
            asteroids.append(Asteroid())
            asteroid_timer = current_time
            asteroid_frequency = max(500, asteroid_frequency - 50)

        for asteroid in asteroids[:]:
            asteroid.move()
            asteroid.draw()
            if asteroid.rect.colliderect(pygame.Rect(spaceship_x, spaceship_y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)):
                print("Game Over!")
                game_over = True
            
            if asteroid.rect.y > SCREEN_HEIGHT:
                asteroids.remove(asteroid)
            
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if bullet.rect.colliderect(asteroid.rect):
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    break
        
        pygame.display.flip()

        clock.tick(60)
    
game()

pygame.quit()