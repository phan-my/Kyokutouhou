import math
from math import cos
import pygame
import pgzrun
from random import randint
from dataclasses import dataclass
PI = 3.141592653589793238462643

# clockwise from top left
@dataclass
class Square:
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
    diagonal = distance*cos(PI/4) - distance
    if keyboard.left and keyboard.down and (inLeft and inDown):
        sprite.x -= diagonal
        sprite.y += diagonal
    if keyboard.left and keyboard.up and (inLeft and inUp):
        sprite.x -= diagonal
        sprite.y -= diagonal
    if keyboard.right and keyboard.up and (inRight and inUp):
        sprite.x += diagonal
        sprite.y -= diagonal
    if keyboard.right and keyboard.down and (inRight and inDown):
        sprite.x += diagonal
        sprite.y += diagonal

def straight_bullet(sprite, speed) -> None:
    sprite.y += speed

TITLE = "Kyokutouhou"
WIDTH = 800
HEIGHT = 600

playground = Square(
    (50 + 16, 470 - 16),
    (30 + 32, 560 - 32),
    (50, 470),
    (30, 560)
)

playgroundWidth = playground.xMargins[1] - playground.xMargins[0]
playgroundHeight = playground.yMargins[1] - playground.yMargins[0]

player = Actor("reimu")
player.x = playground.xMargins[0] + (playgroundWidth/2)
player.y = playground.yMargins[1] - 24
background = Actor("proportional-background")
bullet = Actor("bullet-vertical.png")
bullet.x = randint(playground.xMargins[0], playground.xMargins[1])

def draw():
    background.draw()
    player.draw()
    bullet.draw()

def update(dt):
    movement(player, playground)

    if bullet.y < playground.yBorders[1]:
        straight_bullet(bullet, 3.5)
    else:
        bullet.x = randint(playground.xMargins[0], playground.xMargins[1])
        bullet.y = playground.yBorders[0]

pgzrun.go()
print("Hello, World!")
