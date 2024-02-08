from tkinter import * 
from tkinter.ttk import *
from PIL import Image, ImageTk
import cv2
import numpy as np
import joblib
from pygame import mixer
import menu

class App:
    def __init__(self, width, height, word_list):
        # initialise sound
        mixer.init()
        mixer.music.load("sounds/easter_egg.wav")
        self.playing = 10 


        # initialise camera
        self.camera = cv2.VideoCapture(0)
        self.width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # init main window
        self.window = Tk()
        self.window.title("Easter egg")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.width_menu = width
        self.height_menu = height
        self.word_list = word_list

        # init image recognition window
        self.open = ""
        self.model = joblib.load('cnn_model.pkl')

        # init overlay
        self.overlay = cv2.imread('sprites\\heart.png')
        self.overlay = cv2.resize(self.overlay, (int(self.width), int(self.height)))
        
        #init button
        self.open = 0
        self.alph_text = ["closed palm", "open palm"]


        self.photo = None
        self.init_gui()

        self.delay = 15
        self.update()
        self.window.mainloop()
        

    
    def init_gui(self):
        master = self.window

        l0 = Label(master, text = "Please open your palm for the easter egg", font=("Arial, 20"))
        l0.grid(row = 0, column = 0, columnspan= 3, sticky = "w")

        self.l1 = Label(master, text = self.alph_text[self.open], font=("Arial, 20"))
        self.l1.grid(row = 2, column = 1)

        self.canvas = Canvas(master, width = self.width, height = self.height)
        self.canvas.grid(row = 1, column = 0, columnspan=4, pady = 5)

        
    def on_close(self):
        self.window.destroy()  # Destroy the window
        mixer.music.stop()  # Stop the music
        menu.App(self.width_menu, self.height_menu, self.word_list)  # Open the menu

    
    def update(self):
        alphabets = ['A', 'B', 'C', 'D', 'del', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'nothing', 'O', 'P', 'Q', 'R', 'S', 'space', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        val, frame  = self.camera.read()
        frame = cv2.resize(frame, (200,200))
        frame = frame/255
        proba = self.model.predict(frame.reshape(1,200,200,3), verbose = 0)
        pred = alphabets[np.argsort(proba[0])[-1]]
        if pred == "W" or pred == "Y":
            self.open = 1
        else: self.open = 0
        self.l1.config(text = self.alph_text[self.open])


        val, frame = self.camera.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        added_frame = cv2.addWeighted(frame,0.5,self.overlay, 0.5,0)
        rgb_added_frame = cv2.cvtColor(added_frame, cv2.COLOR_BGR2RGB)

        if val:
            if self.open == 1:
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(rgb_added_frame))
                if self.playing == 0:
                    mixer.music.play()
                    self.playing = 10
                else: self.playing -= 1
            else:
                self.photo = self.photo = ImageTk.PhotoImage(image = Image.fromarray(rgb_frame))
            self.canvas.create_image(0,0,image = self.photo, anchor = NW)

        self.window.after(self.delay, self.update)


def restart_music(self, event):
    mixer.music.rewind()

        