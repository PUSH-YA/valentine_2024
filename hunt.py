import pygame as pg
import random
import enemy
from sys import exit
import menu


GOAL = 28 # 28 months since we started dating
FRAME_LENGTH = 24

class App():

    
    def __init__(self, width, height, enemies):
        clock = pg.time.Clock()
        screen = pg.display.set_mode((width, height))
        is_running = True

        pg.init()
        pg.font.init()
        pg.mouse.set_visible(False)

        pg.mixer.init()
        pg.display.set_caption("HAPPY VALENTINE's DAY 2024, KIRBY")

        # game properties
        self.width = width
        self.height = height
        self.enemies = enemies

        # font
        font_path = "fonts/pixel.ttf"
        self.font = pg.font.Font(font_path, 36)

        # sound
        self.game_sound = pg.mixer.Sound("sounds/loop.mp3")
        self.shoot_sound = pg.mixer.Sound("sounds/shoot.wav")
        self.game_sound.set_volume(0.1)
        self.game_sound.play(-1)

       # score
        self.score = 0
        self.score_text = self.font.render(f"{self.score}", True, (255, 255, 255))

        # enemy + bcg
        self.enemy = enemy.Enemy(self.enemies, self.score, self.width, self.height, False)
        self.explosion = [-1, (0,0)]
        self.bcg_frame = 0

        while is_running:

            # reduce overhead by NOT calling a function for each frame
            if self.bcg_frame < 10:
                frame = "0" + str(self.bcg_frame)
            else:
                frame = str(self.bcg_frame)
            img = pg.image.load("sprites/bcg/f"+ frame + ".png")
            screen.fill((0, 0, 0))
            screen.blit(img, (0, 0))
            self.bcg_frame = (self.bcg_frame + 1)%FRAME_LENGTH
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.shoot_sound.play()
                    pos = pg.mouse.get_pos()
                    if self.enemy.check_collision(pos):
                        self.shoot_enemy()
                        self.explosion = [FRAME_LENGTH, pos]

            #update the enemy
            self.enemy.update(self.width, self.height)

            # render
            self.enemy.draw(screen)
            screen.blit(self.score_text, (15, 10))
            if self.explosion[0] >= 0:
                self.create_explosion(screen)
            self.draw_cursor(screen)

            pg.display.flip()
            clock.tick(60)

        # start the menu app
        self.game_sound.stop()
        menu.App(self.width, self.height, self.enemies)

    
    def draw_cursor(self, canvas):      
        pos = pg.mouse.get_pos()
        img = pg.image.load("sprites/cursor.png")
        canvas.blit(img, pos) # draw the cursor


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

    def create_explosion(self, screen):
        frame_num = self.explosion[0]
        if frame_num < 10:
            frame = "0" + str(frame_num)
        else:
            frame = str(frame_num)
        img = pg.image.load("sprites/explosion/f"+ frame + ".png")
        self.explosion[0] -= 1
        screen.blit(img, self.explosion[1])
            
        

        

            