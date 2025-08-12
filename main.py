import tkinter as tk
from config import *
import os

class File_Renamer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=WINDOW_BG_COLOUR)

        self.setup_widget() # call upon the widgets created
        self.load_txt()
        self.write_to_txt()
        self.root.mainloop()

    def setup_widget(self):
        self.main_address = tk.Text(self.root, height=1, width=75, bg=WIDGET_BOX_COLOUR) # text line for the main address that doesnt change
        self.main_address.place(x=970,y=10)
        self.main_address_save_button = tk.Button(self.root, text="save text", command=self.write_to_txt) # a button for the main address save to txt file
        self.main_address_save_button.place(x=1690,y=10)

        self.search_address = tk.Text(self.root, height=1, width=75, bg=WIDGET_BOX_COLOUR) # serach bar for the LCode or the variable address
        self.search_address.place(x=970,y=40)
        self.search_address_button = tk.Button(self.root, text="show files", command=self.show_directory) # a button for the main address save to txt file
        self.search_address_button.place(x=1690,y=40)

        self.directory_display = tk.Text(self.root, height=50, width=75, bg=WIDGET_BOX_COLOUR)
        self.directory_display.place(x=970,y=90)
        self.directory_display.bind("<Button-1>", self.on_click)

    def rename_file(self):
        print("done")

    def write_to_txt(self):
        text_to_save = self.main_address.get("1.0", tk.END)
        with open("pathfile.txt","w") as file:
            file.write(text_to_save)

    def load_txt(self):
        if os.path.exists("pathfile.txt"):
            with open("pathfile.txt", "r") as file:
                content = file.read()
                self.main_address.insert(tk.END, content)
    
    def show_directory(self):
        self.directory_display.delete("1.0", tk.END)

        main_address = self.main_address.get("1.0", tk.END).strip()
        search_address = self.search_address.get("1.0", tk.END).strip()

        self.directory_path = os.path.join(main_address, search_address) if search_address else main_address
        
        file_name = os.listdir(self.directory_path)
        self.directory_display.delete("1.0", tk.END)
        for file in file_name:
            self.directory_display.insert(tk.END, file + "\n")

    def on_click(self, event):


app = File_Renamer()