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