import math
from math import cos
import pygame
import pgzrun
from pgzero.keyboard import keyboard
PI = 3.141592653589793238462643

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

def reimu_slowdown(player) -> None:
    # Documentation: Built-in Objects
    if keyboard.lshift:
        player.image = "reimu-focus"
    if not keyboard.lshift:
        player.image = "reimu"

# player hitbox is one point in the center of her sprite
def death(Bullets, i, player, bulletsOnScreen, bulletWidth, bulletHeight) -> None:
    for j in range(bulletsOnScreen):
        if Bullets[i+j].x - bulletWidth/2 < player.x < Bullets[i+j].x + bulletWidth/2 and\
        Bullets[i+j].y - bulletHeight/2 < player.y < Bullets[i+j].y + bulletHeight/2:
            exit()
