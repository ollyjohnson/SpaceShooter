import pygame
import random

pygame.init()
pygame.mixer.init()

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

spaceship_img = pygame.image.load("assets/SpaceShipNormal.png").convert_alpha()
asteroid_img = pygame.image.load("assets/Asteroid2.png").convert_alpha()
bullet_img = pygame.image.load("assets/laserBullet.png").convert_alpha()
spaceship_img = pygame.transform.scale(spaceship_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
asteroid_img = pygame.transform.scale(asteroid_img, (ASTEROID_WIDTH, ASTEROID_HEIGHT))
bullet_img = pygame.transform.scale(bullet_img, (BULLET_WIDTH, BULLET_HEIGHT))
background_img = pygame.image.load("assets/back.png").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

shoot_sound = pygame.mixer.Sound("assets/laser1.wav")
shoot_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
explosion_sound.set_volume(0.7)
background_sound = pygame.mixer.Sound("assets/c64_action_loop.wav")
background_sound.set_volume(0.05)


class Bullet:
    
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,BULLET_WIDTH, BULLET_HEIGHT)

    def move(self):
        self.rect.y -= 5
    
    def draw(self):
        screen.blit(bullet_img, self.rect.topleft)
 

class Asteroid:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0,SCREEN_WIDTH-ASTEROID_WIDTH), 0, ASTEROID_WIDTH, ASTEROID_HEIGHT)
        self.speed = random.randint(2,5)

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(asteroid_img, self.rect.topleft)

def dispaly_score(score):
    font = pygame.font.Font(None,36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH-150,10))


def game():
    spaceship_x  = SCREEN_WIDTH // 2
    spaceship_y = SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10
    spaceship_speed = 5
    bullets = []
    asteroids = []
    asteroid_frequency = 2000
    asteroid_timer = 0
    score = 0

    game_over = False

    background_sound.play(loops=-1)

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
            shoot_sound.play()
            bullets.append(Bullet(spaceship_x + SPACESHIP_WIDTH // 2 - BULLET_WIDTH // 2, spaceship_y))
        
        screen.blit(background_img, (0,0))
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
                print(f"Game Over!\nFinal Score: {score}")
                game_over = True
            
            if asteroid.rect.y > SCREEN_HEIGHT:
                asteroids.remove(asteroid)
            
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if bullet.rect.colliderect(asteroid.rect):
                    explosion_sound.play()
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    score += 1
                    break
        
        dispaly_score(score)
        pygame.display.flip()

        clock.tick(60)
    
game()

pygame.quit()