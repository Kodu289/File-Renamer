import tkinter as tk
from config import *
import os

class File_Renamer:
    def __init__(self):
        window = tk.Tk()
        window.title(WINDOW_TITLE)
        window.geometry(WINDOW_SIZE)
        window.configure(bg=WINDOW_BG_COLOUR)

        self.setup_widget() # call upon the widgets created
        window.mainloop()

    def setup_widget(self):
        self.label = tk.label
        print("widget")

    def rename_file(self):
        print("done")


app = File_Renamer()