import math
from math import cos
import pygame
import pgzrun
from random import randint
PI = 3.141592653589793238462643

TITLE = "Kyokutouhou"
WIDTH = 800
HEIGHT = 600

# py equiv of void, stackoverflow/questions/36797282
def movement(sprite) -> None:
    if keyboard.lshift:
        distance = 2
    else:
        distance = 4

    if keyboard.left:
        sprite.x -= distance
    if keyboard.down:
        sprite.y += distance
    if keyboard.up:
        sprite.y -= distance
    if keyboard.right:
        sprite.x += distance

    # diagonal movement same speed as vertical/horizontal
    diagonal = distance*cos(PI/4) - distance
    if keyboard.left and keyboard.down:
        sprite.x -= diagonal
        sprite.y += diagonal
    if keyboard.left and keyboard.up:
        sprite.x -= diagonal
        sprite.y -= diagonal
    if keyboard.right and keyboard.up:
        sprite.x += diagonal
        sprite.y -= diagonal
    if keyboard.right and keyboard.down:
        sprite.x += diagonal
        sprite.y += diagonal

def straight_bullet(sprite, speed) -> None:
    sprite.y += speed

player = Actor("reimu")
background = Actor("black-background-800x600")
bullet = Actor("bullet-vertical-3x6.png")
bullet.x = randint(0, WIDTH)

def draw():
    background.draw()
    player.draw()
    bullet.draw()

def update(dt):
    movement(player)
    if bullet.y < HEIGHT:
        straight_bullet(bullet, 3.5)
    else:
        bullet.x = randint(0, WIDTH)
        bullet.y = 0

pgzrun.go()
print("Hello, World!")
