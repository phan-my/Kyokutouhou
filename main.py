import math
from math import cos
import pygame
import pgzrun
from random import randint
from dataclasses import dataclass
PI = 3.141592653589793238462643

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

# py equiv of void, stackoverflow/questions/36797282
def movement(sprite, area) -> None:
    if keyboard.lshift:
        distance = 2
    else:
        distance = 4
    
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

def straight_bullet(sprite, speed) -> None:
    sprite.y += speed

TITLE = "Kyokutouhou"
WIDTH = 800
HEIGHT = 600

background = Actor("proportional-background")

playground = Rectangle(
    (50 + 16, 470 - 16),
    (30 + 32, 560 - 32),
    (50, 470),
    (30, 560)
)

playgroundWidth = playground.xMargins[1] - playground.xMargins[0]
playgroundHeight = playground.yMargins[1] - playground.yMargins[0]

player = Actor("reimu")
playerWidth = 32
playerHeight = 64
player.x = playground.xMargins[0] + (playgroundWidth/2)
player.y = playground.yMargins[1] - 24

playerHitbox = Rectangle(
    (player.x, player.x),
    (player.y, player.y),
    (player.x - playerWidth/2, player.x + playerWidth/2),
    (player.y - playerHeight/2, player.y + playerHeight/2),
)

bullet = Actor("bullet-vertical.png")
bulletWidth = 6
bulletHeight = 12
bullet.x = randint(playground.xMargins[0], playground.xMargins[1])

def draw():
    background.draw()
    player.draw()
    bullet.draw()
    bullet.draw()

def update(dt):
    movement(player, playground)

    if bullet.y < playground.yBorders[1]:
        straight_bullet(bullet, 3.5)
    else:
        bullet.x = randint(playground.xMargins[0], playground.xMargins[1])
        bullet.y = playground.yBorders[0]
    
    # death
    if bullet.x - bulletWidth/2 < player.x < bullet.x + bulletWidth/2 and\
    bullet.y - bulletHeight/2 < player.y < bullet.y + bulletHeight/2:
        exit()

pgzrun.go()
print("Hello, World!")
