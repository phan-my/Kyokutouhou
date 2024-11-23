from bulletpatterns import *
from mechanics import *
import math
from math import cos, fmod
import time
from time import sleep
import pygame
import pgzrun
from random import randint
from dataclasses import dataclass
PI = 3.141592653589793238462643

# struct-like object for hitboxes and playground
@dataclass
class Rectangle:
    xMargins: (int, int)
    yMargins: (int, int)
    xBorders: (int, int)
    yBorders: (int, int)
    """
    tl: (int, int)
    tr: (int, int)
    br: (int, int)
    bl: (int, int)
    """

TITLE = "Kyokutouhou"
WIDTH = 800
HEIGHT = 600

background = Actor("proportional-background")

# set up player
player = Actor("reimu")
playerWidth = 32
playerHeight = 64

playground = Rectangle(
    (50 + playerWidth/2, 470 - playerWidth/2),
    (30 + playerHeight/2, 560 - playerHeight/2),
    (50, 470),
    (30, 560)
)

playgroundWidth = playground.xMargins[1] - playground.xMargins[0]
playgroundHeight = playground.yMargins[1] - playground.yMargins[0]
player.x = playground.xMargins[0] + (playgroundWidth/2)
player.y = playground.yMargins[1] - 24

playerHitbox = Rectangle(
    (player.x, player.x),
    (player.y, player.y),
    (player.x - playerWidth/2, player.x + playerWidth/2),
    (player.y - playerHeight/2, player.y + playerHeight/2),
)

# set up player's shots
PlayerBullets = []
playerBullets = 16
playerBulletSpeed = 10

for i in range(playerBullets):
    PlayerBullets.append(Actor("player-bullet-red"))
    PlayerBullets[i].pos = player.pos

# set up bullets
Bullets = []
bullets = int(1024*2**(0))

for i in range(bullets):
    Bullets.append(Actor("bullet-vertical.png"))
    Bullets[i].x = randint(playground.xBorders[0], playground.xBorders[1])

bulletWidth = 6
bulletHeight = 12

# set up enemy
Enemies = []
enemies = 128
enemySpeed = 1

enemy01Width = 32
enemy01Height = 32

for i in range(enemies):
    Enemies.append(Actor("enemy-01"))
    Enemies[i].x = randint(playground.xBorders[0], playground.xBorders[1])

# badbox (enemy hitbox)
badHitboxes = bullets + enemies
BadHitbox = []
for bullet in Bullets:
    BadHitbox.append(bullet)

for enemy in Enemies:
    BadHitbox.append(enemies)

# overlay
frame = Actor("frame")

playerLevel = 1

def draw():
    background.draw()
    player.draw()

    # https://electronstudio.github.io/pygame-zero-book/chapters/shooter.html
    for bullet in Bullets:
        bullet.draw()
    
    for enemy in Enemies:
        enemy.draw()
    
    # bullets 
    for j in range(playerBullets):
        PlayerBullets[j].draw()
    
    # draw frame of screen to hide bullets
    frame.draw()


i = 0
start = time.perf_counter()
end = time.perf_counter()
elapsed = end - start

start_level = time.perf_counter()
ticksSincePlayerShot = 0
ticksSinceStart = 0
nthPlayerBullet = 0

def update(dt):
    global player, bullet, i, start, end, elapsed, start_level, enemySpeed, Enemies, enemies, enemy01Width, enemy01Height, playerLevel
    global playerBulletSpeed, ticksSincePlayerShot
    global ticksSinceStart, nthPlayerBullet

    movement(player, playground)
    reimu_slowdown(player)

    for j in range(playerBullets):
        if PlayerBullets[j].y < 0:
            PlayerBullets[j] = Actor("bullet-vertical")
            PlayerBullets[j].pos = player.pos

        # elapsed > 0.1 to prevent startfire
        if PlayerBullets[j].image == "player-bullet-red" and elapsed > 0.1:
            PlayerBullets[j].y -= playerBulletSpeed

    if keyboard.z:
        ticksSincePlayerShot += 1
        # if fmod(j + ticksSincePlayerShot*playerBullets/dt, 5) == 0:
        if ticksSinceStart % 3 == 0:
            PlayerBullets[nthPlayerBullet].image = "player-bullet-red"
            nthPlayerBullet = (nthPlayerBullet + 1) % playerBullets 
    
    if not keyboard.z:
        for j in range(playerBullets):
            if PlayerBullets[j].image != "player-bullet-red":
                PlayerBullets[j].pos = player.pos
                PlayerBullets[j].image = "bullet-vertical"
        ticksSincePlayerShot = 0

    lap = time.perf_counter()
    elapsed_lap = lap - start_level


    # clock.schedule_interval(update_straight_bullet, 2.0)
    random_straight_bullet(Bullets, 4.5, playground, elapsed)

    # enemy behavior
    activeEnemies = 16
    interval = 2
    enemySpeed = 1
    k = 0
    while k < activeEnemies:
        if (k/interval)*(elapsed/activeEnemies) + 1 >= interval:
#            print((k/interval)*(elapsed/bulletsOnScreen))
            update_straight_bullet(Enemies, k, enemySpeed, playground)
        k += 1
    
    death(Bullets, i, player, bullets, bulletWidth, bulletHeight)
    death(Enemies, i, player, enemies, enemy01Width, enemy01Height)

    if elapsed >= 50 and i < bullets - 2 - 1:
        # print(elapsed)
        for j in range(bullets):
            Bullets[i+j].x = 9001
        i += bulletsOnScreen
        start = time.perf_counter()
        elapsed = 0
    end = time.perf_counter()
    elapsed = end - start

    ticksSinceStart += 1
    
# clock.schedule(draw_nth_straight_bullet, 0.5)
pgzrun.go()
print("Hello, World!")
