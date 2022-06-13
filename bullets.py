from constants import player_bullet_sprites, enemy_bullet_sprites, \
    screen_height, small_explosion_sprites
from misc_sprites import Explosion
from pygame import sprite


class Player_bullet(sprite.Sprite):
    def __init__(self, pos_x, pos_y, sprites=player_bullet_sprites):
        super().__init__()
        self.sprites = sprites
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect.y -= 30
        if self.rect.y > screen_height or self.rect.y < 0:
            self.kill()

    def collide_with_enemy(self, enemy, explosions_sprites):
        enemy.lose_life(explosions_sprites)
        explosions_sprites.add(
            Explosion(self.rect.x, self.rect.y, small_explosion_sprites))
        self.kill()


class Enemy_bullet(sprite.Sprite):
    def __init__(
        self, pos_x, pos_y, a, b, left_or_right, sprites=enemy_bullet_sprites
    ):
        super().__init__()
        self.sprites = sprites
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.a = a
        self.b = b
        self.left_or_right = left_or_right

    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        if self.a != 0 and self.b != 0:
            self.rect.x = self.rect.x + self.left_or_right*5
            self.rect.y = self.a*self.rect.x + self.b
        else:
            self.rect.y += 11
        if self.rect.y > screen_height or self.rect.y < 0:
            self.kill()
