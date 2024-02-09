import pygame as pg
from sys import exit

# x,y,dx,dy
start_NDCS = [0.35,0.2,0.3,0.1]# 0 to 1
vr_NDCS = [0.15,0.7,0.25,0.1]# 0 to 1
easter_NDCS = [0.55,0.7,0.25,0.1]# 0 to 1

HOVER_COL = (177,177,239)
TEXT_HOVER = (38,38,187)
NO_HOVER_COL = (255,255,255)
TEXT_NO_HOVER = (0,0,0)

FRAME_LENGTH = 24

class App():
    def __init__(self,width, height, word_list):
        self.width = width
        self.height = height
        self.buttons = None
        self.bcg_frame = 0
        self.exit = False

        #init & global var
        pg.init()
        pg.mixer.init()
        pg.font.init()
        pg.mouse.set_visible(False)
        canvas = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("HAPPY VALENTINE 2024")
        hover = [False, False, False]

        # font
        font_path = "fonts/pixel.ttf"
        self.font = pg.font.Font(font_path, 36)

        # add buttons
        self.place_buttons()

        # sound
        self.game_sound = pg.mixer.Sound("sounds/loop.mp3")
        self.shoot_sound = pg.mixer.Sound("sounds/shoot.wav")
        self.game_sound.set_volume(0.1)
        self.game_sound.play(-1)
        
        while not self.exit:
            
            # reduce overhead by NOT calling a function for each frame
            if self.bcg_frame < 10:
                frame = "0" + str(self.bcg_frame)
            else:
                frame = str(self.bcg_frame)
            img = pg.image.load("sprites/bcg/f"+ frame + ".png")
            canvas.fill((0, 0, 0))
            canvas.blit(img, (0, 0))
            self.bcg_frame = (self.bcg_frame + 1)%FRAME_LENGTH

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit = True
                if event.type == pg.MOUSEMOTION:
                    pos = pg.mouse.get_pos()
                    hover = self.check_button(pos)
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.shoot_sound.play()
                    pos = pg.mouse.get_pos()
                    clicked = self.check_button(pos)
                    self.button_actions(clicked, word_list)

            self.colour_buttons(hover, canvas)
            self.draw_cursor(canvas)
            pg.display.update()
    
    def draw_cursor(self, canvas):      
        pos = pg.mouse.get_pos()
        img = pg.image.load("sprites/cursor.png")
        canvas.blit(img, pos) # draw the cursor


    def place_buttons(self):
        start_button = pg.Surface((start_NDCS[2] * self.width, start_NDCS[3] * self.height))
        start_button.fill(NO_HOVER_COL)
        vr_button = pg.Surface((vr_NDCS[2] * self.width, vr_NDCS[3] * self.height))
        vr_button.fill(NO_HOVER_COL)
        easter_button = pg.Surface((easter_NDCS[2] * self.width, easter_NDCS[3] * self.height))
        easter_button.fill(NO_HOVER_COL)
        
        self.buttons_rect = [
        pg.Rect((start_NDCS[0] * self.width, start_NDCS[1] * self.height, start_NDCS[2] * self.width, start_NDCS[3] * self.height)),
        pg.Rect((vr_NDCS[0] * self.width, vr_NDCS[1] * self.height, vr_NDCS[2] * self.width, vr_NDCS[3] * self.height)),
        pg.Rect((easter_NDCS[0] * self.width, easter_NDCS[1] * self.height, easter_NDCS[2] * self.width, easter_NDCS[3] * self.height))
        ]
        
        self.buttons = [start_button, vr_button, easter_button]

    def check_button(self, pos):
        hover = [False, False, False]
        for i, button in enumerate(self.buttons_rect):
            if button.collidepoint(pos):
                hover[i] = True
        return hover
    
    def colour_buttons(self, hover, canvas):
        corner_radius = self.height*0.1//2
        for i, button in enumerate(self.buttons):
            if hover[i]:
                button.fill(HOVER_COL)
                colour = HOVER_COL
                # Add titles for each button
                if i == 0:
                    text = self.font.render("Start!", True, TEXT_HOVER)
                elif i == 1:
                    text = self.font.render("VR minigame", True, TEXT_HOVER)
                elif i == 2:
                    text = self.font.render("Easter egg", True, TEXT_HOVER)
                
            else:
                button.fill(NO_HOVER_COL)
                colour = NO_HOVER_COL
                # Add titles for each button
                if i == 0:
                    text = self.font.render("Start!", True, TEXT_NO_HOVER)
                elif i == 1:
                    text = self.font.render("VR minigame", True, TEXT_NO_HOVER)
                elif i == 2:
                    text = self.font.render("Easter egg", True, TEXT_NO_HOVER)    
            # button bcg
            canvas.blit(button, self.buttons_rect[i].topleft) 
            # button txt
            canvas.blit(text, (self.buttons_rect[i].topleft[0] + self.buttons_rect[i].width/2 - text.get_width()/2, 
                                self.buttons_rect[i].topleft[1] + self.buttons_rect[i].height/2 - text.get_height()/2))
            pg.draw.circle(canvas, colour, (self.buttons_rect[i].topleft[0], 
                                            self.buttons_rect[i].topleft[1] + corner_radius), corner_radius)
            pg.draw.circle(canvas, colour, (self.buttons_rect[i].topleft[0] + self.buttons_rect[i].width, 
                                            self.buttons_rect[i].topleft[1] + corner_radius), corner_radius)
            
    def button_actions(self, clicked, word_list):
        import main
        action = next((i for i, value in enumerate(clicked) if value), None)
        if action is not None:
            pg.quit()
            if action == 0:
                main.open_hunt(self.width, self.height, word_list)
            if action == 1:
                main.open_compviz(self.width, self.height, word_list)
            if action == 2:
                main.open_easter(self.width, self.height, word_list)

        

        


