import math
from math import cos
import pygame
import pgzrun
from pgzero.keyboard import keyboard
from pgzero.actor import Actor
PI = 3.141592653589793238462643

# allow keyboard arrow control of sprite in area
def movement(sprite, area) -> None:
    # `-> None' is py equiv of void, stackoverflow/questions/36797282
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

# lshift for slow movement of sprite
def slowdown(sprite) -> None:
    # Documentation: Built-in Objects
    if keyboard.lshift:
        sprite.image = "reimu-focus"
    if not keyboard.lshift:
        sprite.image = "reimu"

# z for firing own bullets; use as nthPlayerBullet = shooting(...)
def shooting(PlayerBullets, playerBulletCount, nthPlayerBullet, player, ticksSincePlayerShot):
    playerBulletSpeed = 8

    for i in range(playerBulletCount):
        if PlayerBullets[i].y < 0:
            PlayerBullets[i].image = "blank"
            PlayerBullets[i].pos = player.pos
        if PlayerBullets[i].image != "player-bullet-red":
            PlayerBullets[i].pos = player.pos

        # elapsed > 0.1 to prevent startfire
        if PlayerBullets[i].image == "player-bullet-red":
            PlayerBullets[i].y -= playerBulletSpeed

    if keyboard.z:
        # if fmod(j + ticksSincePlayerShot*playerBullets/dt, 5) == 0:
        if ticksSincePlayerShot % 6 == 0:
            PlayerBullets[nthPlayerBullet].image = "player-bullet-red"
            nthPlayerBullet = (nthPlayerBullet + 1) % playerBulletCount 
    return nthPlayerBullet

# player hitbox is one point in the center of her sprite
def death(EnemySprites, i, player, enemySpriteCount, enemyWidth, enemyHeight) -> None:
    for j in range(enemySpriteCount):
        if EnemySprites[i+j].x - enemyWidth/2 < player.x < EnemySprites[i+j].x + enemyWidth/2 and\
        EnemySprites[i+j].y - enemyHeight/2 < player.y < EnemySprites[i+j].y + enemyHeight/2:
            exit()
