
import random
from numpy import ones, vstack
from numpy.linalg import lstsq
from pygame import sprite
from misc_sprites import Explosion
from constants import enemy_size, player_size, homing_enemy_sprites, \
    shooting_straight_enemy_sprites, shooting_multiple_enemy_sprites, \
    big_explosion_sprites
from bullets import Enemy_bullet


class Enemy(sprite.Sprite):
    def __init__(
            self, LIVES, dest_y, sprites, pos_x, pos_y,
            bullet_type=Enemy_bullet):
        super().__init__()
        self.sprites = sprites
        self.LIVES = LIVES
        self.dest_y = dest_y
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.bullet_type = bullet_type

    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        if self.rect.y < self.dest_y:
            self.rect.y += 5

    def lose_life(self, explosions_sprites):
        if self.LIVES > 0:
            self.LIVES = self.LIVES - 1
        else:
            explosions_sprites.add(
                Explosion(self.rect.x, self.rect.y, big_explosion_sprites))
            self.kill()


class Enemy_homing_misiles(Enemy):

    def __init__(self, pos_x, pos_y, LIVES, dest_y):
        super().__init__(LIVES, dest_y, homing_enemy_sprites, pos_x, pos_y)

    def load_bullets(self, pos_x, pos_y):
        bullets = []
        if self.rect.y >= self.dest_y:
            if self.rect.x - pos_x < 0:
                left_or_right = 1
            else:
                left_or_right = -1
            if abs(
                (self.rect.x - enemy_size[0]/2) -
                (pos_x - player_size[0]/2)
                        ) < player_size[0]:
                bullets.append((self.bullet_type(
                    self.rect.x, self.rect.y, 0, 0, left_or_right)))
            else:
                points = [(self.rect.x, self.rect.y +
                           enemy_size[1]), (pos_x, pos_y)]
                x_coords, y_coords = zip(*points)
                A = vstack([x_coords, ones(len(x_coords))]).T
                a, b = lstsq(A, y_coords)[0]
                bullets.append(self.bullet_type(
                    self.rect.x, self.rect.y, a, b, left_or_right))
        return bullets


class Enemy_shooting_straight(Enemy):

    def __init__(self, pos_x, pos_y, LIVES, dest_y):
        super().__init__(
            LIVES, dest_y, shooting_straight_enemy_sprites, pos_x, pos_y)

    def load_bullets(self, pos_x, pos_y):
        bullets = []
        if self.rect.y >= self.dest_y:
            bullets.append(self.bullet_type(
                self.rect.x + enemy_size[0]/2, self.rect.y + enemy_size[1], 0,
                0, 1
                ))
        return bullets


class Enemy_shooting_multiple(Enemy):

    def __init__(self, pos_x, pos_y, LIVES, dest_y):
        super().__init__(
            LIVES, dest_y, shooting_multiple_enemy_sprites, pos_x, pos_y)

    def load_bullets(self, pos_x, pos_y):
        bullets = []
        for i in range(0, 7):
            pos_x = pos_x - random.randint(0, round(player_size[0]))
            if self.rect.y >= self.dest_y:
                if self.rect.x - pos_x < 0:
                    left_or_right = 1
                else:
                    left_or_right = -1
                if abs(
                        (self.rect.x - enemy_size[0]/2) -
                        (pos_x - player_size[0]/2)
                        ) < player_size[0]:
                    bullets.append(self.bullet_type(
                        self.rect.x, self.rect.y, 0, 0, left_or_right))
                else:
                    points = [(self.rect.x, self.rect.y +
                               enemy_size[1]), (pos_x, pos_y)]
                    x_coords, y_coords = zip(*points)
                    A = vstack([x_coords, ones(len(x_coords))]).T
                    a, b = lstsq(A, y_coords)[0]
                    bullets.append(self.bullet_type(
                        self.rect.x, self.rect.y, a, b, left_or_right))
        return bullets
