import os
from pygame import transform, image
import ctypes
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
player_size = [screen_width/20, screen_height/10]
enemy_size = [screen_width/18, screen_height/8]

death_screen = transform.scale(image.load(
    os. getcwd()+'/sprites/death_screen.png'), (screen_width, screen_height))


def explosion_sprites_gen(size):
    explosion_sprites = []
    boom = image.load(os. getcwd()+'/sprites/boom.png')
    for horizontal in range(0, 6):
        for vertical in range(0, 7):
            explosion_sprites.append(
                transform.scale(
                    boom.subsurface(
                        (240*vertical, 240*horizontal), (240, 240)), [
                            size[0], size[1]]))
    return explosion_sprites


small_explosion_sprites = explosion_sprites_gen([20, 20])
big_explosion_sprites = explosion_sprites_gen(enemy_size)


player_bullet_sprites = []
player_bullet_sprites.append(
    transform.scale(image.load(
        os. getcwd()+'/sprites/bullet.png'), [10, 50]))
player_bullet_sprites.append(
    transform.scale(image.load(
        os. getcwd()+'/sprites/bullet.png'), [15, 50]))
player_bullet_sprites.append(
    transform.scale(image.load(
        os. getcwd()+'/sprites/bullet.png'), [20, 50]))
player_bullet_sprites.append(
    transform.scale(image.load(
        os. getcwd()+'/sprites/bullet.png'), [15, 50]))

enemy_bullet = image.load(os. getcwd()+'/sprites/ball.png')
enemy_bullet = enemy_bullet.subsurface((100, 100), (100, 100))
enemy_bullet_sprites = []
enemy_bullet_sprites.append(
    transform.scale(
        enemy_bullet, [screen_width/80, screen_height/40]))
enemy_bullet_sprites.append(
    transform.scale(
        enemy_bullet, [screen_width/80, screen_height/40]))
enemy_bullet_sprites.append(
    transform.scale(
        enemy_bullet, [screen_width/80, screen_height/40]))
enemy_bullet_sprites.append(
    transform.scale(
        enemy_bullet, [screen_width/80, screen_height/40]))

homing_enemy_sprites = []
homing_enemy_sprites.append(
    transform.scale(image.load(
        os. getcwd()+'/sprites/enemy_homing1.png'), enemy_size))
homing_enemy_sprites.append(
    transform.scale(image.load(
        os. getcwd()+'/sprites/enemy_homing2.png'), enemy_size))

shooting_straight_enemy_sprites = []
shooting_straight_enemy_sprites.append(
    transform.scale(image.load(
        os. getcwd()+'/sprites/enemy_straight1.png'), enemy_size))
shooting_straight_enemy_sprites.append(
    transform.scale(image.load(
        os. getcwd()+'/sprites/enemy_straight2.png'), enemy_size))

shooting_multiple_enemy_sprites = []
shooting_multiple_enemy_sprites.append(
    transform.scale(image.load(
        os. getcwd()+'/sprites/enemy_multiple1.png'), enemy_size))
shooting_multiple_enemy_sprites.append(
    transform.scale(image.load(
        os. getcwd()+'/sprites/enemy_multiple2.png'), enemy_size))
