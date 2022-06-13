
from pygame import sprite


class Explosion(sprite.Sprite):
    def __init__(self, pos_x, pos_y, sprites):
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
            self.kill()
        self.image = self.sprites[self.current_sprite]
