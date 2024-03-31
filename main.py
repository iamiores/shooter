#IMPORTS
import time
import pygame.display
from random import randint
from pygame import *
import sys


#ALTERNATES
missed = 0
shot = 0
hit = 0
max_shot = 15
max_missed = 5
max_hit = 3


"""CLASSES"""


class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_width, sprite_height, sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (sprite_width, sprite_height))
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y
        self.speed = sprite_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        # pygame.draw.rect(window, (255, 255, 255), self.rect, 2)
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x <= window_width - 100:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x >= 20:
            self.rect.x -= self.speed
        if keys[K_w] and self.rect.y >= window_height - 200:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y <= window_height - 110:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet(image_bullet, self.rect.centerx - 10, self.rect.top - 10, 25, 30, 15)
        bullets.add(bullet)

    def big_fire(self):
        big_bullet = Bullet(image_big_bullet, self.rect.centerx - 15, self.rect.top - 55, 30, 60, 10)
        big_bullets.add(big_bullet)


class Enemy(GameSprite):
    def update(self):
        # pygame.draw.rect(window, (0, 0, 255), self.rect, 2)
        self.rect.y += self.speed
        global missed
        if self.rect.y >= window_height:
            self.rect.x = randint(50, window_width - 80)
            self.rect.y = 0
            missed += 1


class Bullet(GameSprite):
    def update(self):
        # pygame.draw.rect(window, (255, 0, 255), self.rect, 2)
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


class Asteroid(GameSprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_width, sprite_height, sprite_speed):
        super().__init__(sprite_image, sprite_x, sprite_y, sprite_width, sprite_height, sprite_speed)
        self.angle = 0

    def update(self):
        # pygame.draw.rect(window, (0, 255, 255), self.rect, 2)
        self.rect.y += self.speed
        global missed
        if self.rect.y >= window_height:
            self.rect.x = randint(50, window_width - 80)
            self.rect.y = 0
            missed += 1
            self.angle = 0
        self.angle += self.speed

        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        window.blit(rotated_image, self.rect.topleft)


#DISPLAY SETTINGS
window_width = 700
window_height = 500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Shooter')

#MUSIC & SOUND
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.1)

#FONT & TEXT
font.init()
font1 = font.Font('fonts/Retro Gaming.ttf', 26)
font2 = font.Font('fonts/Retro Gaming.ttf', 50)
# font1 = font.SysFont('Arial', 26)
# font2 = font.SysFont('Arial', 50)
text_win = font2.render('YOU WIN!', True, (255, 255, 255))
text_lose = font2.render('YOU LOSE!', True, (180, 0, 0))

#IMAGES
image_bg = 'images/bg.png'
bg = transform.scale(image.load(image_bg), (window_width, window_height))
image_player = 'images/rocket.png'
image_enemy = 'images/ufo.png'
image_bullet = 'images/bullet.png'
image_big_bullet = 'images/big_bullet.png'
image_asteroid = 'images/asteroid.png'
image_icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(image_icon)

#SPRITE GROUPS
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(image_enemy, randint(50, window_width - 80), 0, 90, 60, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Asteroid(image_asteroid, randint(50, window_width - 80),  0, 80, 50, randint(1, 6))
    asteroids.add(asteroid)


bullets = sprite.Group()
big_bullets = sprite.Group()

#PLAYER
player = Player(image_player, window_width / 2, window_height - 100, 80, 100, 10)

'''GAME CYCLE'''
game = True
finish = False
FPS = 30
clock = time.Clock()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if bullets.__len__() < 3:
                    player.fire()
                    fire_sound.play()
            if e.key == K_e:
                if big_bullets.__len__() < 1:
                    player.big_fire()
                    fire_sound.play()

    if not finish:
        window.blit(bg, (0, 0))
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        big_bullets.draw(window)
        text_missed = font1.render('MISSED: ' + str(missed), 1, (255, 255, 255))
        text_shot = font1.render('SHOT: ' + str(shot), 1, (255, 255, 255))
        window.blit(text_missed, (10, 50))
        window.blit(text_shot, (10, 80))
        bullets.update()
        big_bullets.update()
        player.update()
        monsters.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            shot += 1
            monster = Enemy(image_enemy, randint(50, window_width - 80), 0, 80, 50, randint(1, 5))
            monsters.add(monster)

        collides = sprite.groupcollide(monsters, big_bullets, True, True)
        for collide in collides:
            shot += 1
            monster = Enemy(image_enemy, randint(50, window_width - 80), 0, 80, 50, randint(1, 5))
            monsters.add(monster)

        if shot >= 5:
            asteroids.update()
        if sprite.spritecollide(player, asteroids, False):
            hit += 1
        if hit >= max_hit:
            finish = True
            window.blit(text_lose, (200, 200))

        if sprite.spritecollide(player, monsters, False) or missed >= max_missed:
            finish = True
            window.blit(text_lose, (200, 200))
        if shot >= max_shot:
            finish = True
            window.blit(text_win, (200, 200))

        display.update()
    clock.tick(FPS)