from tkinter import * 
from tkinter.ttk import *
import os
from PIL import Image, ImageTk
import cv2
import camera
import os
import threading
import numpy as np
import joblib
import pyttsx3

class App:



    def __init__(self):
        # initialise camera
        self.camera = cv2.VideoCapture(0)
        self.width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)


        self.window = Tk()

        self.window.title = "ASL to Text/Speech"


        self.alph_text = ""
        self.text = ""
        self.model = joblib.load('cnn_model.pkl')

        self.overlay = cv2.imread('heart.png')
        self.overlay = cv2.resize(self.overlay, (int(self.width), int(self.height)))    
        self.speechbutton = Button(self.window, command=self.speak)
        self.speechbutton.grid(row = 3, column = 3, sticky = E)

        self.init_gui()

        self.delay = 15
        self.update()

        self.window.bind("<Return>",self.on_enter_key)
        self.window.bind("<BackSpace>",self.backspace)

        
        self.window.mainloop()
        

    
    def init_gui(self):
        master = self.window

        l0 = Label(master, text = "Please use the ENTER key to confirm letter and BACKSPACE to delete the letter")
        l0.grid(row = 0, column = 0, columnspan= 3)
        self.canvas = Canvas(master, width = self.width, height = self.height)
        self.canvas.grid(row = 1, column = 0, columnspan=4, pady = 5)

        l1 = Label(master, text = "Alph Text")
        l2 = Label(master, text = "Text")
        
        self.alph_label = Label(master, width = 100,relief = "groove")
        self.text_label = Label(master, width = 100,relief = "groove")
        self.alph_label.grid(row = 2, column = 1)
        self.text_label.grid(row = 3, column = 1)

        # grid method to arrange labels in respective
        # rows and columns as specified
        l1.grid(row = 2, column = 0,  sticky = W, padx =2, pady = 2)
        l2.grid(row = 3, column = 0,  sticky = W, padx = 2, pady =2 )
        
        # entry widgets, used to take entry from user
        # e1 = Entry(master,width=50)
        # e2 = Entry(master,width=100)
        
        # # this will arrange entry widgets
        # e1.grid(row = 2, column = 1)
        # e2.grid(row = 3, column = 1)
        
        
        # button widget
        # self.autobutton = Button(master, text = "Autocomplete")
        
        
        # # arranging button widgets
        # self.autobutton.grid(row = 2, column = 3, sticky = E)


    
    def update(self):
        alphabets = ['A', 'B', 'C', 'D', 'del', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'nothing', 'O', 'P', 'Q', 'R', 'S', 'space', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        val, frame  = self.camera.read()
        frame = cv2.resize(frame, (200,200))
        frame = frame/255
        proba = self.model.predict(frame.reshape(1,200,200,3), verbose = 0)
        pred = alphabets[np.argsort(proba[0])[-1]]
        # pred = "A" # TODO change it to model predict based on image
        self.alph_text = pred
        self.text_label.config(text = self.text)
        self.alph_label.config(text = self.alph_text)


        val, frame = self.camera.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        added_frame = cv2.addWeighted(frame,0.5,self.overlay, 0.5,0)
        rgb_added_frame = cv2.cvtColor(added_frame, cv2.COLOR_BGR2RGB)

        if val:
            if self.alph_text == "W":
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(rgb_added_frame))
            else:
                self.photo = self.photo = ImageTk.PhotoImage(image = Image.fromarray(rgb_frame))
            self.canvas.create_image(0,0,image = self.photo, anchor = NW)

        self.window.after(self.delay, self.update)

    
    def on_enter_key(self,event):
        if (self.alph_text == "space"):
            self.text+=" "
        elif(self.alph_text == "nothing"):
            self.alph_text = ""
        elif(self.alph_text == "del"):
            self.backspace()
        else:
            self.text += self.alph_text
        self.alph_text = ""

    def backspace(self,event):
        if (len(self.text) != 0):self.text = self.text[:len(self.text)-1]
    
    def speak_voice(self):
        self.voice.say(self.text)
        self.voice.runAndWait()
        self.voice.stop()

    def speak(self):
        threading.Thread(target=self.speak_voice).start()

        