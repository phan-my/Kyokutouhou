import pygame
import pgzrun

# straight-falling bullet with parameter sprite and speed
def straight_bullet(sprite, speed) -> None:
    sprite.y += speed

# extended straight_bullet() with anti-out-of-bounds redundancy
def update_straight_bullet(bullet, speed, playground) -> None:
    if bullet.y < playground.yBorders[1] or bullet.image != "1x1":
        straight_bullet(bullet, speed)
    # if out of bounds, nullify and reposition on y-axis
    else:
        bullet.image = "1x1"
        bullet.y = -20

# use as nthBullet = random_straight_bullet(...) 
def random_straight_bullet(Bullets, bulletCount, nthBullet, image, playground, speed, interval, ticksSinceStart):
    # timing setup with interval
    if ticksSinceStart % interval == 0:
        Bullets[nthBullet].image = image
        nthBullet = (nthBullet + 1) % bulletCount
    
    # idea: bullets fall if they are not 1x1.png
    for bullet in Bullets:
        if bullet.image != "1x1":
            update_straight_bullet(bullet, speed, playground)
        if bullet.y > 600:
            bullet.y = 0 
            bullet.image = "1x1"

    return nthBullet

# all enemy01 are created equal
def random_enemy01(Enemies, enemyCount, nthEnemy, playground, ticksSinceStart):
    speed = 2
    interval = 16
    enemySpeed = 1

    # timing setup with interval
    if ticksSinceStart % interval == 0:
        Enemies[nthEnemy].image = "enemy-01"
        nthEnemy = (nthEnemy + 1) % enemyCount
    
    # idea: enemies fall if they are not 1x1.png
    for enemy in Enemies:
        if enemy.image != "1x1":
            update_straight_bullet(enemy, speed, playground)
        if enemy.y > 600:
            enemy.image = "1x1"
    
    return nthEnemy