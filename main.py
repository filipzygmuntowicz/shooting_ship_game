import random
import pygame
import math
from constants import screen_width, screen_height, player_size, enemy_size, \
    death_screen
from starfield import Starfield
from enemy import Enemy_homing_misiles, Enemy_shooting_straight, \
     Enemy_shooting_multiple
from player import Player


class Timer:

    def __init__(self):
        self.current_time = pygame.time.get_ticks()

    def get_elapsed_time(self):
        now = pygame.time.get_ticks()
        elapsed_time = (now - self.current_time) * 0.001
        self.current_time = now
        return elapsed_time


clock = pygame.time.Clock()

if __name__ == "__main__":
    pygame.init()
    font = pygame.font.SysFont('system', 32)

    NUMBER_OF_STARS = 250
    STARTING_ANGLE = 90
    CLOSEST_STAR_COLOR = (255, 255, 255)
    STAR_SIZE_IN_PIXELS = 1
    preset_speeds = (((100, 10), (300, 30)))
    current_speed = 1

    # For fullscreen, replace pygame.SWSURFACE with pygame.FULLSCREEN

    display = pygame.display.set_mode(
        (screen_width, screen_height), pygame.SWSURFACE)

    my_starfield = Starfield(display, display.get_rect(), NUMBER_OF_STARS,
                             STARTING_ANGLE, preset_speeds[current_speed],
                             Timer,
                             STAR_SIZE_IN_PIXELS, CLOSEST_STAR_COLOR)
    player_bullets_sprites = pygame.sprite.Group()
    enemy_bullets_sprites = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    enemy_homing_sprite = pygame.sprite.Group()
    enemy_straight_sprite = pygame.sprite.Group()
    enemy_multiple_sprite = pygame.sprite.Group()
    explosions_sprites = pygame.sprite.Group()
    player = Player(0, screen_height/1.1, 15)
    timer = Timer()
    player_sprite.add(player)

    PLAYER_SHOOT = pygame.USEREVENT + 0
    ENEMY_HOMING_SHOOT = pygame.USEREVENT + 1
    ENEMY_STRAIGHT_SHOOT = pygame.USEREVENT + 2
    ENEMY_MULTIPLE_SHOT = pygame.USEREVENT + 3
    pygame.time.set_timer(PLAYER_SHOOT, 150)
    pygame.time.set_timer(ENEMY_HOMING_SHOOT, 1000)
    pygame.time.set_timer(ENEMY_STRAIGHT_SHOOT, 500)
    pygame.time.set_timer(ENEMY_MULTIPLE_SHOT, 2000)

    def enemy_shoot(player, enemy):
        bullets = enemy.load_bullets(player.rect.x, player.rect.y)
        for bullet in bullets:
            enemy_bullets_sprites.add(bullet)

    def player_shoot():
        bullets = player.load_bullets(player.rect.x, player.rect.y)
        for bullet in bullets:
            player_bullets_sprites.add(bullet)

    def next_stage(stage):
        global score
        global how_many_waves
        if player.LIVES < 15:
            player.LIVES += min(2*min(1, round(stage/4)), 15-player.LIVES)
        if stage == 0:
            how_many_waves = 1
        elif stage < 5:
            score = score + stage*10000
        elif stage >= 5 and stage < 15:
            score = score + stage*50000
            player.how_many_shots = 2
        elif stage >= 15 and stage < 20:
            score = score + stage*100000
            player.how_many_shots = 4
            how_many_waves = 2
        elif stage > 20:
            score = score + stage*200000
        pygame.time.set_timer(ENEMY_HOMING_SHOOT, 1000 -
                              min(500, math.floor((stage/2))*50))
        pygame.time.set_timer(ENEMY_STRAIGHT_SHOOT, 500 -
                              min(250, math.floor((stage/2))*25))
        pygame.time.set_timer(ENEMY_MULTIPLE_SHOT, 2000 -
                              min(1000, math.floor((stage/2))*100))
        pygame.time.set_timer(PLAYER_SHOOT, 150 -
                              min(100, math.floor((stage/2))*10))
        for i in range(0, how_many_waves):
            how_many_homing = random.randint(1, min(2+math.floor(stage/4), 7))
            how_many_straight = random.randint(
                1, min(2+math.floor(stage/4), 7))
            how_many_multiple = random.randint(
                1, min(2+math.floor(stage/4), 7))
            how_many = how_many_homing+how_many_multiple+how_many_straight
            interval = 18/how_many
            enemy_intervals = []
            enemies = []
            for i in range(how_many):
                enemy_intervals.append(i*interval*enemy_size[0])
            for i in range(how_many_homing):
                enemies.append(Enemy_homing_misiles(
                    1, -200, 5 + min(13, stage + 3),
                    screen_height/(random.randint(7, 22))))
            for i in range(how_many_straight):
                enemies.append(Enemy_shooting_straight(
                    1, -200, 5 + min(10, stage),
                    screen_height/(random.randint(7, 22))))
            for i in range(how_many_multiple):
                enemies.append(Enemy_shooting_multiple(
                    1, -200, 5 + min(15, stage + 10),
                    screen_height/(random.randint(7, 22))))
            random.shuffle(enemies)
            for i in range(how_many):
                enemies[i].rect.x = enemy_intervals[i]
            for enemy in enemies:
                if enemy.__class__.__name__ == "Enemy_homing_misiles":
                    enemy_homing_sprite.add(enemy)
                elif enemy.__class__.__name__ == "Enemy_shooting_straight":
                    enemy_straight_sprite.add(enemy)
                elif enemy.__class__.__name__ == "Enemy_shooting_multiple":
                    enemy_multiple_sprite.add(enemy)
    stage = 0
    flash = 0
    score = 0
    how_many_waves = 1
    next_stage(stage)
    while 1:
        my_starfield.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            raise SystemExit
        if keys[pygame.K_d]:
            if player.rect.x < screen_width:
                player.rect.x = player.rect.x+screen_width/(80)
        # Ruch gracza w lewo
        if keys[pygame.K_a]:
            if player.rect.x > 0:
                player.rect.x = player.rect.x-screen_width/(80)
        # Ruch gracza do góry
        if keys[pygame.K_w]:
            if player.rect.y > 0:
                player.rect.y = player.rect.y-screen_width/80
        # Ruch gracza w dół
        if keys[pygame.K_s]:
            if player.rect.y < screen_height:
                player.rect.y = player.rect.y+screen_width/80
        if keys[pygame.K_SPACE]:
            for event in pygame.event.get():
                if event.type == PLAYER_SHOOT and player.LIVES > 0:
                    player_shoot()
                if event.type == ENEMY_HOMING_SHOOT:
                    for enemy in enemy_homing_sprite.sprites():
                        enemy_shoot(player, enemy)
                if event.type == ENEMY_STRAIGHT_SHOOT:
                    for enemy in enemy_straight_sprite.sprites():
                        enemy_shoot(player, enemy)
                if event.type == ENEMY_MULTIPLE_SHOT:
                    for enemy in enemy_multiple_sprite.sprites():
                        enemy_shoot(player, enemy)
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                raise SystemExit
            if event.type == ENEMY_HOMING_SHOOT:
                for enemy in enemy_homing_sprite.sprites():
                    enemy_shoot(player, enemy)
            if event.type == ENEMY_STRAIGHT_SHOOT:
                for enemy in enemy_straight_sprite.sprites():
                    enemy_shoot(player, enemy)
            if event.type == ENEMY_MULTIPLE_SHOT:
                for enemy in enemy_multiple_sprite.sprites():
                    enemy_shoot(player, enemy)
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_p]:
                    for enemy in enemy_homing_sprite.sprites():
                        enemy.kill()
                    for enemy in enemy_straight_sprite.sprites():
                        enemy.kill()
                    for enemy in enemy_multiple_sprite.sprites():
                        enemy.kill()
                    stage = stage + 1
        enemy_bullets_sprites.draw(display)
        enemy_bullets_sprites.update()
        player_bullets_sprites.draw(display)
        player_bullets_sprites.update()
        player_sprite.update()
        player_sprite.draw(display)
        enemy_homing_sprite.update()
        enemy_straight_sprite.update()
        enemy_multiple_sprite.update()
        enemy_homing_sprite.draw(display)
        enemy_straight_sprite.draw(display)
        enemy_multiple_sprite.draw(display)
        if len(enemy_homing_sprite.sprites()) == 0 and \
            len(enemy_straight_sprite.sprites()) == 0 and \
                len(enemy_multiple_sprite.sprites()) == 0:
            stage = stage + 1
            next_stage(stage)
        explosions_sprites.draw(display)
        explosions_sprites.update()
        for bullet in player_bullets_sprites.sprites():
            for enemy in enemy_homing_sprite.sprites():
                if pygame.sprite.collide_rect(bullet, enemy):
                    bullet.collide_with_enemy(enemy, explosions_sprites)
            for enemy in enemy_straight_sprite.sprites():
                if pygame.sprite.collide_rect(bullet, enemy):
                    bullet.collide_with_enemy(enemy, explosions_sprites)
            for enemy in enemy_multiple_sprite.sprites():
                if pygame.sprite.collide_rect(bullet, enemy):
                    bullet.collide_with_enemy(enemy, explosions_sprites)
        player_hitbox = pygame.Rect.copy(player.rect)
        pygame.Rect.inflate_ip(
            player_hitbox, -player_size[0]/1.1, -player_size[1]/1.1)
        for bullet in enemy_bullets_sprites.sprites():
            if pygame.Rect.colliderect(player_hitbox, bullet.rect):
                bullet.kill()
                player.lose_life(explosions_sprites)
        if player.LIVES == 0:
            player_sprite.empty()
            if flash == 0:
                display.fill((255, 255, 255))
                flash = 1
            display.blit(death_screen, (0, 0))
            if keys[pygame.K_r]:
                for enemy in enemy_homing_sprite.sprites():
                    enemy.kill()
                for enemy in enemy_straight_sprite.sprites():
                    enemy.kill()
                for enemy in enemy_multiple_sprite.sprites():
                    enemy.kill()
                enemy_homing_sprite.empty()
                enemy_straight_sprite.empty()
                enemy_multiple_sprite.empty()
                stage = 0
                flash = 0
                score = 0
                player = Player(0, screen_height/1.1, 15)
                player_sprite.add(player)
                next_stage(stage)
        if player.LIVES > 0:
            score = score + random.randint(1, 10)
        score_text = font.render(
            'SCORE:' + str(score).replace(".0", ""), True, (255, 255, 255))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (screen_width/30, screen_height/25)
        lives_text = font.render(
            'LIVES:' + str(player.LIVES), True, (255, 255, 255))
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.center = (screen_width/30, screen_height/17)
        display.blit(score_text, score_text_rect)
        display.blit(lives_text, lives_text_rect)
        pygame.display.update()
        display.fill((0, 0, 0))
        clock.tick(60)
