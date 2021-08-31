import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("./images/background.jpg")
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("./images/ufo.png")
pygame.display.set_icon(icon)


player_img = pygame.image.load("./images/space-invaders.png")
player_x = 370
player_y = 480
player_x_change = 0


bullet_img = pygame.image.load("./images/bullet.png")
bullet_x = 0
bullet_y = 480
bullet_y_change = 2
bullet_state = "ready"


enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("./images/enemy.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.3)
    enemy_y_change.append(40)


enemy_bullet_img = pygame.image.load("./images/bullet.png")
enemy_bullet_x = 0
enemy_bullet_y = 480
enemy_bullet_x_change = 0
enemy_bullet_y_change = 2
enemy_bullet_state = "ready"

score = 0
font = pygame.font.Font("freesansbold.ttf", 30)
textX = 10
textY = 10

game_over_font = pygame.font.Font("freesansbold.ttf", 69)


def show_score(x, y):
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))


def game_over_text():
    game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x, y+10))


def enemy_fire_bullet(x, y):
    global enemy_bullet_state
    enemy_bullet_state = "fire"
    screen.blit(enemy_bullet_img, (x, y+10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) +
                         math.pow(enemy_y - bullet_y, 2))
    if distance < 20:
        return True
    else:
        return False


# game loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.7
            elif event.key == pygame.K_RIGHT:
                player_x_change = 0.7
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(player_x, bullet_y)

                    #enemy is going to fire a bullet at the same time
                    for i in range(num_of_enemies):
                        if enemy_bullet_state == "ready":
                            enemy_bullet_x = enemy_x[i]
                            enemy_bullet_y = enemy_y[i]
                            enemy_fire_bullet(enemy_x[i], enemy_y[i])
                            break
                    
                    #enemy_bullet_x = enemy_x[1]
                    #enemy_bullet_y = enemy_y[1]
                    #enemy_fire_bullet(enemy_x[1], enemy_y[1])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 769:
        player_x = 769

    for i in range(num_of_enemies):
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -0.3
            enemy_y[i] += enemy_y_change[i]

        collison = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collison:
            bullet_y = 480
            bullet_state = "ready"
            enemy_bullet_state = "ready"
            
            score += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
        enemy(enemy_x[i], enemy_y[i], i)

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        enemy_fire_bullet(enemy_bullet_x, enemy_bullet_y)
        enemy_bullet_y += enemy_bullet_y_change

    #create the same logic for the enemy_bullet, but starting from the enemy_bullet_x
    
    # if enemy_bullet_y <= 480:
    #    enemy_bullet_y = enemy_y

    player(player_x, player_y)
    show_score(textX, textY)
    pygame.display.update()
