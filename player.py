from pygame import image, transform, sprite
import os
from constants import player_size, small_explosion_sprites, \
    big_explosion_sprites
from bullets import Player_bullet
from misc_sprites import Explosion


class Player(sprite.Sprite):
    def __init__(self, pos_x, pos_y, LIVES, bullet_type=Player_bullet):
        super().__init__()
        self.sprites = []
        self.sprites.append(
            transform.scale(image.load(
                os. getcwd()+'/sprites/player1.png'), player_size))
        self.sprites.append(
            transform.scale(image.load(
                os. getcwd()+'/sprites/player2.png'), player_size))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.LIVES = LIVES
        self.how_many_shots = 1
        self.bullet_type = bullet_type

    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

    def lose_life(self, explosions_sprites):
        if self.LIVES > 0:
            self.LIVES = self.LIVES - 1
            explosions_sprites.add(
                Explosion(self.rect.x, self.rect.y, small_explosion_sprites))
        else:
            explosions_sprites.add(
                Explosion(self.rect.x, self.rect.y, big_explosion_sprites))
            self.kill()

    def load_bullets(self, pos_x, pos_y):
        bullets = []
        if self.how_many_shots == 1:
            bullets.append(self.bullet_type(pos_x + player_size[0]/2, pos_y))
        elif self.how_many_shots == 2:
            bullets.append(self.bullet_type(pos_x, pos_y))
            bullets.append(self.bullet_type(pos_x + player_size[0], pos_y))
            return bullets
        elif self.how_many_shots == 4:
            bullets.append(self.bullet_type(pos_x, pos_y))
            bullets.append(self.bullet_type(pos_x + player_size[0]/4, pos_y))
            bullets.append(self.bullet_type(pos_x + 3*player_size[0]/4, pos_y))
            bullets.append(self.bullet_type(pos_x + player_size[0], pos_y))
        return bullets
