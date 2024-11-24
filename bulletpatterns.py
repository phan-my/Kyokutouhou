import pygame
import pgzrun

# straight-falling bullet with parameter sprite and speed
def straight_bullet(sprite, speed) -> None:
    sprite.y += speed

def update_straight_bullet(bullet, speed, playground) -> None:
    if bullet.y < playground.yBorders[1] or bullet.image != "blank":
        straight_bullet(bullet, speed)
    else:
        bullet.x = 9001
        # Bullets[i].y = playground.yBorders[0]

# use as n = random_straight_bullet(...) 
def random_straight_bullet(Bullets, bulletCount, nthBullet, playground, speed, interval, ticksSinceStart):
    # clock.schedule_interval(update_straight_bullet, 2.0)
    """            PlayerBullets[nthPlayerBullet].image = "player-bullet-red"
            nthPlayerBullet = (nthPlayerBullet + 1) % playerBulletCount 
    for k in range(bulletsOnScreen):
        if (k/interval)*(elapsed/bulletsOnScreen) + 1 >= interval:"""
    bulletsOnScreen = bulletCount/2

    if ticksSinceStart % interval == 0:
        Bullets[nthBullet].image = "bullet-vertical"
        nthBullet = (nthBullet + 1) % bulletCount
    
    for bullet in Bullets:
        if bullet.image != "1x1":
            update_straight_bullet(bullet, speed, playground)   
    return nthBullet

# all enemy01 are created equal
def random_enemy01(Enemies, enemyCount, nthEnemy, playground, ticksSinceStart):
    speed = 2
    interval = 16
    enemySpeed = 1

    if ticksSinceStart % interval == 0:
        Enemies[nthEnemy].image = "enemy-01"
        nthEnemy = (nthEnemy + 1) % enemyCount
    
    for enemy in Enemies:
        if enemy.image != "1x1":
            update_straight_bullet(enemy, speed, playground)
    
    return nthEnemy