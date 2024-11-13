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

# `-> None' is py equiv of void, stackoverflow/questions/36797282
def movement(sprite, area) -> None:
    if keyboard.lshift:
        distance = 2.5
    else:
        distance = 5
    
    # define sprite in boundaries of area
    inLeft = sprite.x > area.xMargins[0]
    inDown = sprite.y < area.yMargins[1]
    inUp = sprite.y > area.yMargins[0]
    inRight = sprite.x < area.xMargins[1]

    if keyboard.left and inLeft:
        sprite.x -= distance
    if keyboard.down and inDown:
        sprite.y += distance
    if keyboard.up and inUp:
        sprite.y -= distance
    if keyboard.right and inRight:
        sprite.x += distance

    # diagonal movement same speed as vertical/horizontal
    # diagonal movement scraping border results in slowdown
    diagonal = distance*cos(PI/4) - distance

    if keyboard.left and keyboard.down:
        if inDown:
            sprite.y += diagonal
        if inLeft:
            sprite.x -= diagonal
    if keyboard.left and keyboard.up:
        if inLeft:
            sprite.x -= diagonal
        if inUp:
            sprite.y -= diagonal
    if keyboard.right and keyboard.up:
        if inRight:
            sprite.x += diagonal
        if inUp:
            sprite.y -= diagonal
    if keyboard.right and keyboard.down:
        if inRight:
            sprite.x += diagonal
        if inDown:
            sprite.y += diagonal

# straight-falling bullet with parameter sprite and speed
def straight_bullet(sprite, speed) -> None:
    sprite.y += speed

TITLE = "Kyokutouhou"
WIDTH = 800
HEIGHT = 600

background = Actor("proportional-background")
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

Bullets = []

bullets = 1024*10

for i in range(bullets):
    Bullets.append(Actor("bullet-vertical.png"))
    Bullets[i].x = randint(playground.xBorders[0], playground.xBorders[1])

bulletWidth = 6
bulletHeight = 12

def draw():
    background.draw()
    player.draw()

    # https://electronstudio.github.io/pygame-zero-book/chapters/shooter.html
    for bullet in Bullets:
        bullet.draw()

i = 0
start = time.time()
end = time.time()
elapsed = end - start

def update_straight_bullet(i):
    if Bullets[i].y < playground.yBorders[1]:
        straight_bullet(Bullets[i], 4.5)
    else:
        Bullets[i].x = 9001
        # Bullets[i].y = playground.yBorders[0]

start_level = time.time()
def update(dt):
    global player, bullet, i, start, end, elapsed, start_level
    movement(player, playground)
    
    # Documentation: Built-in Objects
    if keyboard.lshift:
        player.image = "reimu-focus"
    if not keyboard.lshift:
        player.image = "reimu"

    # clock.schedule_interval(update_straight_bullet, 2.0)
    bulletsOnScreen = 1024

    lap = time.time()
    elapsed_lap = lap - start_level

    k = 0
    interval = 2

    while k < bulletsOnScreen:
        if (k/interval)*(elapsed/bulletsOnScreen) >= interval:
            print((k/interval)*(elapsed/bulletsOnScreen))
            update_straight_bullet(k)
        k += 1

    # death
    for j in range(bulletsOnScreen):
        if Bullets[i+j].x - bulletWidth/2 < player.x < Bullets[i+j].x + bulletWidth/2 and\
        Bullets[i+j].y - bulletHeight/2 < player.y < Bullets[i+j].y + bulletHeight/2:
            exit()

    if elapsed >= 50 and i < bullets - 2 - 1:
        # print(elapsed)
        for j in range(bulletsOnScreen):
            Bullets[i+j].x = 9001
        i += bulletsOnScreen
        start = time.time()
        elapsed = 0
    end = time.time()
    elapsed = end - start
    
# clock.schedule(draw_nth_straight_bullet, 0.5)
pgzrun.go()
print("Hello, World!")
