import pygame as pg
import random
import enemy
from sys import exit
import menu


GOAL = 28 # 28 months since we started dating

class App():

    
    def __init__(self, width, height, enemies):
        clock = pg.time.Clock()
        screen = pg.display.set_mode((width, height))
        is_running = True

        pg.init()
        pg.font.init()

        pg.display.set_caption("HAPPY VALENTINE's DAY 2024, KIRBY")
        self.width = width
        self.height = height
        self.enemies = enemies
        font_path = "fonts/pixel.ttf"
        self.font = pg.font.Font(font_path, 36)

        self.score = 0
        self.score_text = self.font.render(f"{self.score}", True, (255, 255, 255))

        self.enemy = enemy.Enemy(self.enemies, self.score, self.width, self.height, False)

        while is_running:
            screen.fill((0, 0, 0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if self.enemy.rect.collidepoint(pos):
                        self.shoot_enemy()

            #update the enemy
            self.enemy.update(self.width, self.height)

            # render
            self.enemy.draw(screen)
            screen.blit(self.score_text, (15, 10))
            pg.display.flip()
            clock.tick(60)

        # start the menu app
        menu.App(self.width, self.height, self.enemies)

    def shoot_enemy(self):
        self.enemy.health -= 1
        if self.enemy.health <= 0: # kill the enemy
            self.score += 1
        
        if self.score >= GOAL:
            self.score_text = self.font.render(f"28 months! and more", True, (255, 255, 255))
            WIN = True
        else:
            self.score_text = self.font.render(f"{self.score}", True, (255, 255, 255))
            WIN = False
            
        self.enemy = enemy.Enemy(self.enemies, self.score, self.width, self.height, WIN)
            
        

        

            