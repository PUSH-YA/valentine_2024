####### to disable the verbose in ###############################################
####### tensorflow before any imports ###############################################
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' 
####################################################################################

import menu
import compviz
import easter_egg
import hunt
import subprocess


# this will help dealing with circular imports

def open_menu(WIDTH, HEIGHT, word_list):
    menu.App(WIDTH, HEIGHT, word_list)

def open_compviz(WIDTH, HEIGHT,word_list):
    compviz.App(WIDTH, HEIGHT,word_list)

def open_easter(WIDTH, HEIGHT,word_list):
    easter_egg.App(WIDTH, HEIGHT, word_list)

def open_hunt(WIDTH, HEIGHT, word_list):    
    hunt.App(WIDTH, HEIGHT, word_list)


if __name__ == "__main__":
    subprocess.run(["pip", "install", "-r", "requirements.txt"])
    word_list = ["frustration", "school", "adult duties", "depression", "self doubt", "hatred", "finding job"]
    WIDTH = 1200
    HEIGHT = 720
    # open_menu(WIDTH, HEIGHT, word_list)