import tkinter as tk
from config import *
import os

class File_Renamer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title(WINDOW_TITLE)
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(bg=WINDOW_BG_COLOUR)

        
        self.setup_widget() # call upon the widgets created
        self.load_txt()
        self.write_to_txt()
        self.window.mainloop()

    def setup_widget(self):
        self.text_box = tk.Text(self.window, height=5, width=50)
        self.text_box.place(x=10,y=10)

        self.button = tk.Button(self.window, text="save text", command=self.write_to_txt)
        self.button.place(x=10,y=100)

    def rename_file(self):
        print("done")

    def write_to_txt(self):
        text_to_save = self.text_box.get("1.0", tk.END)
        with open("pathfile.txt","w") as file:
            file.write(text_to_save)

    def load_txt(self):
        if os.path.exists("pathfile.txt"):
            with open("pathfile.txt", "r") as file:
                content = file.read()
                self.text_box.insert(tk.END, content)

app = File_Renamer()