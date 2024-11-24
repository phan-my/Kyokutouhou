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

""" The types of hitboxes.
    (P)layer
        - vulnerable to badboxes
    (PB)PlayerBullets
        - attacks enemies
    (G)oodbox
        - heals player
    (B)adbox
        - attacks player
        - 2 subtypes:
        Enemy
            - vulnerable to player bullets
        Bullets
            - attack player
    (S)tage
        - inert
"""

TITLE = "Kyokutouhou"
WIDTH = 800
HEIGHT = 600

# set up background
background = Actor("proportional-background")

# set up player
player = Actor("reimu")
playerWidth = 32
playerHeight = 64

# set up scene
playground = Rectangle(
    (50 + playerWidth/2, 470 - playerWidth/2),
    (30 + playerHeight/2, 560 - playerHeight/2),
    (50, 470),
    (30, 560)
)

playgroundWidth = playground.xMargins[1] - playground.xMargins[0]
playgroundHeight = playground.yMargins[1] - playground.yMargins[0]

playerHitbox = Rectangle(
    (player.x, player.x),
    (player.y, player.y),
    (player.x - playerWidth/2, player.x + playerWidth/2),
    (player.y - playerHeight/2, player.y + playerHeight/2),
)

# position player
player.x = playground.xMargins[0] + (playgroundWidth/2)
player.y = playground.yMargins[1] - 24

# set up player's shots
PlayerBullets = []
playerBulletCount = 16
playerBulletWidth = 6
playerBulletHeight = 12
playerLevel = 1
nthPlayerBullet = 0

for i in range(playerBulletCount):
    PlayerBullets.append(Actor("1x1"))
    PlayerBullets[i].pos = player.pos

# set up bullets
Bullets = []
bulletCount = int(1024*2**(0))
bulletWidth = 6
bulletHeight = 12
nthBullet = 0

for i in range(bulletCount):
    Bullets.append(Actor("1x1"))
    Bullets[i].x = randint(playground.xBorders[0], playground.xBorders[1])

# set up enemy
Enemies = []
enemyCount = 128
enemySpeed = 2
nthEnemy = 0
enemy01Width = 32
enemy01Height = 32

for i in range(enemyCount):
    Enemies.append(Actor("1x1"))
    Enemies[i].x = randint(playground.xBorders[0], playground.xBorders[1])
    Enemies[i].y = -enemy01Height

# set up boss
boss = Actor("boss")
bossWidth = 32
bossHeight = 64
boss.x = playground.xMargins[0] + (playgroundWidth/2)
boss.y = bossHeight + int(bossHeight*0.1)
bossHealth = 1024

# badbox (enemy hitbox)
badHitboxCount = bulletCount + enemyCount
BadHitbox = []
for bullet in Bullets:
    BadHitbox.append(bullet)

for enemy01 in Enemies:
    BadHitbox.append(enemyCount)

# overlay
frame = Actor("frame")

def draw():
    background.draw()
    player.draw()

    # https://electronstudio.github.io/pygame-zero-book/chapters/shooter.html
    for bullet in Bullets:
        bullet.draw()
    
    for enemy in Enemies:
        enemy.draw()
    
    # bullets 
    for playerBullet in PlayerBullets:
        playerBullet.draw()
    
    boss.draw()
    
    # draw frame of screen to hide bullets
    frame.draw()

# timing
i = 0
start = time.perf_counter()
end = time.perf_counter()
elapsed = end - start
startLevel = time.perf_counter()
timeSinceStart_s = time.time()
ticksSinceStart = 0
ticksSincePlayerShot = 0

# "ticks" refer to dt
def update(dt):
    global player, start, end, elapsed, startLevel, playerLevel
    global enemySpeed, Enemies, enemyCount, nthEnemy, enemy01Width, enemy01Height
    global ticksSincePlayerShot, ticksSinceStart
    global playerBulletWidth, playerBulletHeight, nthPlayerBullet
    global nthBullet
    global bossHealth
        
    # player mechanics
    movement(player, playground)
    slowdown(player)

    if keyboard.z:
        ticksSincePlayerShot += 1
    if not keyboard.z:
        ticksSincePlayerShot = 0
    
    if ticksSinceStart != 0:
        nthPlayerBullet = shooting(PlayerBullets, playerBulletCount, nthPlayerBullet, player, ticksSincePlayerShot)
    
    lap = time.perf_counter()
    elapsed_lap = lap - startLevel

    # clock.schedule_interval(update_straight_bullet, 2.0)
    nthBullet = random_straight_bullet(Bullets, bulletCount, nthBullet, playground, 4.5, 2, ticksSinceStart)

    # enemy behavior
    activeEnemies = 16
    nthEnemy = random_enemy01(Enemies, enemyCount, nthEnemy, playground, ticksSinceStart)
                
    # killing enemies
    enemy_death(Enemies, enemy01Width, enemy01Height, PlayerBullets)
    
    # damaging boss
    bossHealth = boss_damage(boss, bossWidth, bossHeight, bossHealth, PlayerBullets)
    
    if bossHealth <= 0:
        print("???: Oouuuuuch!")
        print("You win!")
        exit()

    death(Bullets, player, bulletCount, bulletWidth, bulletHeight)
    death(Enemies, player, enemyCount, enemy01Width, enemy01Height)

    if elapsed >= 50 and i < bulletCount - 2 - 1:
        # print(elapsed)
        for j in range(bulletCount):
            Bullets[i+j].x = 9001
        i += bulletsOnScreen
        start = time.perf_counter()
        elapsed = 0
    end = time.perf_counter()
    elapsed = end - start

    ticksSinceStart += 1
    
# clock.schedule(draw_nth_straight_bullet, 0.5)
pgzrun.go()
