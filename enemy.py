import random as rd
import pygame as pg

FONT_SIZE = 36
ENEMY_HEIGHT = 42

class Enemy:

    def __init__(self,  word_list, score, width, height, WIN):

        pg.init()
        pg.font.init()
        
        font_path = "fonts/pixel.ttf"
        self.font = pg.font.Font(font_path, FONT_SIZE)

        if WIN:
            self.name = "We Made it!"
        else:
            self.name = rd.choice(word_list)

        self.width = len(self.name) * FONT_SIZE
        self.x = rd.randint(0, width - self.width)
        self.y = rd.randint(0, height - self.width)
        self.dx = rd.choice([-1, 1])*score//2
        self.dy = rd.choice([-1, 1])*score//2

        self.rect = pg.Rect(self.x, self.y, self.width, ENEMY_HEIGHT)
        self.health = 1

    def draw(self, screen):
        pg.draw.rect(screen, (255, 255, 255), self.rect)
        text = self.font.render(self.name, True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.x + self.width/2, self.y + ENEMY_HEIGHT/2))
        screen.blit(text, text_rect)

    def update(self, width, height):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x, self.y)

        if self.x <= 0 or self.x >= width - self.width:
            self.dx *= -1
        if self.y <= 0 or self.y >= height - ENEMY_HEIGHT:
            self.dy *= -1
        

    

        