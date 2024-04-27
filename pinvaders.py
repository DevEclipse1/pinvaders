import pygame
import time
import random
import ctypes

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("pinvaders")

run = True

x, y = 0, 0
dx, dy = 0, 0

player = pygame.image.load("rocket.png")

enemies = []
bullets = []

lastspawntime = 0

score = 0
hp = 3

def shoot():
    bullets.append(
        [
            pygame.image.load("bullet.png"),
            [x, y]
        ]
    )

font = pygame.font.SysFont("arial.ttf",16)

while run:
    scoretext = font.render(str(score) + " score", True, (0,255,0), (0, 0, 0, 0))
    hptext = font.render(str(hp) + " hp", True, (255, 0,0), (0, 0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -5 
            elif event.key == pygame.K_RIGHT:
                dx = 5 
            elif event.key == pygame.K_UP:
                dy = -5 
            elif event.key == pygame.K_DOWN:
                dy = 5
            elif event.key == pygame.K_SPACE:
                shoot()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                dx = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                dy = 0

    x += dx
    y += dy

    x = max(0, min(x, 800 - player.get_width()))
    y = max(0, min(y, 600 - player.get_height()))

    screen.fill((0, 0, 0))
    screen.blit(player, (x, y))

    if lastspawntime <= time.time():
        lastspawntime = time.time() + 0.5
        enemies.append(
            [
                pygame.image.load("enemy.png") ,
                (random.randint(0,784),-30)
            ]
        )
    
    for enemy in enemies:
        screen.blit(enemy[0], enemy[1])
        pos = list(enemy[1])
        pos[1] += 1
        enemy[1] = tuple(pos)
    
                
        enemy_rect = pygame.Rect(enemy[1][0], enemy[1][1], enemy[0].get_width(), enemy[0].get_height())
        player_rect = pygame.Rect(x, y, player.get_width(), player.get_height())
        
        if enemy_rect.colliderect(player_rect):
            hp -= 1
            enemies.remove(enemy)

    for bullet in bullets:
        screen.blit(bullet[0], bullet[1])
        pos = list(bullet[1])
        pos[1] -= 10
        bullet[1] = tuple(pos)
        
        bullet_rect = pygame.Rect(bullet[1][0], bullet[1][1], bullet[0].get_width(), bullet[0].get_height())
        screen.blit(bullet[0], bullet[1])
        pos = list(bullet[1])
        pos[1] -= 4
        bullet[1] = tuple(pos)

        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[1][0], enemy[1][1], enemy[0].get_width(), enemy[0].get_height())
            if bullet_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
    
    screen.blit(hptext, (10, 10))
    screen.blit(scoretext, (10, 30))
    
    if hp <= 0:
        ctypes.windll.user32.MessageBoxW(0, f"You lost, final score {score}", "Pinvaders", 1)
        run = False
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
