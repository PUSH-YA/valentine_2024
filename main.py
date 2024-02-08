import menu
import compviz
import easter_egg
import hunt
import os


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
    word_list = ["frustration", "school", "adult duties", "depression", "self doubt", "hatred", "finding job"]
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    WIDTH = 1200
    HEIGHT = 720
    open_compviz(WIDTH, HEIGHT, word_list)