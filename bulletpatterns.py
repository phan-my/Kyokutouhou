import pygame
import pgzrun

# straight-falling bullet with parameter sprite and speed
def straight_bullet(sprite, speed) -> None:
    sprite.y += speed

def update_straight_bullet(Bullets, i, speed, playground) -> None:
    if Bullets[i].y < playground.yBorders[1] or Bullets[i].image != "blank":
        straight_bullet(Bullets[i], speed)
    else:
        Bullets[i].x = 9001
        # Bullets[i].y = playground.yBorders[0]

def random_straight_bullet(Bullets, bulletCount, nthBullet, playground, ticksSinceStart):
    # clock.schedule_interval(update_straight_bullet, 2.0)
    """            PlayerBullets[nthPlayerBullet].image = "player-bullet-red"
            nthPlayerBullet = (nthPlayerBullet + 1) % playerBulletCount 
    for k in range(bulletsOnScreen):
        if (k/interval)*(elapsed/bulletsOnScreen) + 1 >= interval:"""
    bulletsOnScreen = bulletCount/2
    interval = 3
    speed = 4.5
    if ticksSinceStart % 2 == 0:
        Bullets[nthBullet].image = "bullet-vertical"
        nthBullet = (nthBullet + 1) % bulletCount
    
    for bullet in Bullets:
        if bullet.image != "1x1":
            straight_bullet(bullet, speed)    
    return nthBullet
