import math
from math import cos
import pygame
import pgzrun
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

player = Actor("reimu")
background = Actor("black-background-800x600")
bullet = Actor("bullet-vertical-3x6.png")

def draw():
    background.draw()
    player.draw()

def update(dt):
    movement(player)

pgzrun.go()
print("Hello, World!")
