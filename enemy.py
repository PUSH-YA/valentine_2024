import random as rd
import pygame as pg

FONT_SIZE = 32
ENEMY_HEIGHT = 56
ENEMY_COLOUR =  (133, 6, 6)
ENEMY_TEXT_COL = (221, 164, 72)
GOAL = 28

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

        self.width = int(len(self.name)*0.8) * FONT_SIZE
        self.x = rd.randint(0, width - self.width)
        self.y = rd.randint(0, height - self.width)
        self.dx = min(rd.choice([-1, 1])*score//3, GOAL//3)
        self.dy = min(rd.choice([-1, 1])*score//3, GOAL//3)

        self.rect = pg.Rect(self.x, self.y, self.width, ENEMY_HEIGHT)
        self.health = 1

    def draw(self, screen):
        corner_radius = ENEMY_HEIGHT//2
        pg.draw.rect(screen, ENEMY_COLOUR, self.rect)
        text = self.font.render(self.name, True, ENEMY_TEXT_COL)
        text_rect = text.get_rect(center=(self.x + self.width/2, self.y + ENEMY_HEIGHT/2))
        pg.draw.circle(screen, ENEMY_COLOUR, (self.x, self.y+ corner_radius), corner_radius)
        pg.draw.circle(screen, ENEMY_COLOUR, (self.x + self.width, self.y + corner_radius), corner_radius)
        screen.blit(text, text_rect)

    def check_collision(self, pos):
        return self.x - ENEMY_HEIGHT <= pos[0] <= self.x + self.width + ENEMY_HEIGHT and self.y <= pos[1] <= self.y + ENEMY_HEIGHT

    def update(self, width, height):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x, self.y)

        if self.x <= 0 or self.x >= width - self.width:
            self.dx *= -1
        if self.y <= 0 or self.y >= height - ENEMY_HEIGHT:
            self.dy *= -1
        

    

        