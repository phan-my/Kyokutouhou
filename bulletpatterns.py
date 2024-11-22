import pygame
import pgzrun

# straight-falling bullet with parameter sprite and speed
def straight_bullet(sprite, speed) -> None:
    sprite.y += speed

def update_straight_bullet(Bullets, i, speed, playground) -> None:
    if Bullets[i].y < playground.yBorders[1]:
        straight_bullet(Bullets[i], speed)
    else:
        Bullets[i].x = 9001
        # Bullets[i].y = playground.yBorders[0]

def random_straight_bullet(Bullets, speed, playground, elapsed):
    # clock.schedule_interval(update_straight_bullet, 2.0)
    bulletsOnScreen = 512
    interval = 3
    
    for k in range(bulletsOnScreen):
        if (k/interval)*(elapsed/bulletsOnScreen) + 1 >= interval:
            print((k/interval)*(elapsed/bulletsOnScreen))
            update_straight_bullet(Bullets, k, speed, playground)
