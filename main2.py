import time

import pygame.display
from random import randint
from pygame import *
missed = 0
shooted = 0


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
        pass


class Enemy(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        global missed
        if self.rect.y <= 0:
            self.rect.x = randint(50, window_width - 80)
            self.rect.y = window_height
            missed += 1


window_width = 700
window_height = 500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Shooter')


mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()


font.init()
font1 = font.Font(None, 36)


image_bg = 'galaxy.jpg'
image_player = 'rocket.png'
image_enemy = 'ufo.png'


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(image_enemy, randint(50, window_width - 80), 500, 80, 50, randint(1, 5))
    monsters.add(monster)


player = Player(image_player, window_width / 2, window_height - 100, 80, 100, 10)

bg = transform.scale(image.load(image_bg), (window_width, window_height))

run = True
finish = False
FPS = 30
clock = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:
        window.blit(bg, (0, 0))
        player.reset()
        monsters.draw(window)
        text_missed = font1.render('Пропущено: ' + str(missed), 1, (255, 255, 255))
        text_shooted = font1.render('Збито: ' + str(shooted), 1, (255, 255, 255))
        window.blit(text_missed, (window_height + 20, 50))
        window.blit(text_shooted, (10, 50))
        player.update()
        monsters.update()
        display.update()
    clock.tick(FPS)
