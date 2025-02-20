import math
from math import cos
import pygame
import pgzrun
from pgzero.keyboard import keyboard
from pgzero.actor import Actor
PI = 3.141592653589793238462643

# arrow control of sprite in area;
def movement(sprite, area) -> None:
    # `-> None' is py equiv of void, stackoverflow/questions/36797282

    # set speed;
    # shift to focus with sprite change
    # Documentation: Built-in Objects
    if keyboard.lshift:
        sprite.image = "reimu-focus"
        distance = 2.5
    else:
        sprite.image = "reimu"
        distance = 5
    
    # define sprite in boundaries of area
    inLeft = sprite.x > area.xMargins[0]
    inDown = sprite.y < area.yMargins[1]
    inUp = sprite.y > area.yMargins[0]
    inRight = sprite.x < area.xMargins[1]

    # set bound for sprite
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


# z for firing own bullets;
# use as nthPlayerBullet = shooting(...)
def shooting(PlayerBullets, playerBulletCount, nthPlayerBullet, player, ticksSincePlayerShot):
    playerBulletSpeed = 8

    for i in range(playerBulletCount):
        if PlayerBullets[i].y < 0:
            PlayerBullets[i].image = "1x1"
            PlayerBullets[i].pos = player.pos
        if PlayerBullets[i].image != "player-bullet-red":
            PlayerBullets[i].pos = player.pos

        # elapsed > 0.1 to prevent startfire
        if PlayerBullets[i].image == "player-bullet-red":
            PlayerBullets[i].y -= playerBulletSpeed

    if keyboard.z:
        if ticksSincePlayerShot % 6 == 0:
            PlayerBullets[nthPlayerBullet].image = "player-bullet-red"
            nthPlayerBullet = (nthPlayerBullet + 1) % playerBulletCount 
    
    return nthPlayerBullet

# rm enemies hit by player bullets
def enemy_death(Enemies, enemyWidth, enemyHeight, PlayerBullets):
    for enemy01 in Enemies:
        for playerBullet in PlayerBullets:
            # since enemy's hitbox is way larger than the player's, it is
            # easier to write in the perspective of the enemy -- sort of a
            # passive tense;
            # if enemy hitbox hits core playerbullet: ...
            if enemy01.x - enemyWidth/2 < playerBullet.x < enemy01.x + enemyWidth/2 and\
            enemy01.y - enemyHeight/2 < playerBullet.y < enemy01.y + enemyHeight/2 and \
            enemy01.image != "1x1" and playerBullet.image != "1x1":
                enemy01.image = "1x1"
                playerBullet.image = "1x1"

                # reposition enemy
                enemy01.y = -enemyHeight

# reduce boss health when hit;
# use as bossHealth = boss_damage(...)
def boss_damage(boss, bossWidth, bossHeight, bossHealth, PlayerBullets):
    for playerBullet in PlayerBullets:
        if boss.x - bossWidth/2 < playerBullet.x < boss.x + bossWidth/2 and\
        boss.y - bossHeight/2 < playerBullet.y < boss.y + bossHeight/2 and \
        playerBullet.image != "1x1":
            bossHealth -= 1
            playerBullet.image = "1x1"

    return bossHealth

# reduce player HP when hit;
# use as playerHealth = death(...)
def death(EnemySprites, enemySpriteCount, enemyWidth, enemyHeight, player, playerHealth) -> None:
    # player hitbox is one point in the center of her sprite
    for j in range(enemySpriteCount):
        if EnemySprites[j].x - enemyWidth/2 < player.x < EnemySprites[j].x + enemyWidth/2 and\
        EnemySprites[j].y - enemyHeight/2 < player.y < EnemySprites[j].y + enemyHeight/2 and\
        EnemySprites[j].image != "1x1":
            return playerHealth - 1

    return playerHealth
