from PIL import Image, ImageTk
import tkinter as tk
import os
import fitz  # PyMuPDF
import io

class JuicyAdventureApp:
    def __init__(self, root):
        self.root = root
        root.geometry("1920x1080")
        root.configure(bg="lightgray")
        root.title("cupcake's juicy adventure")
        
        self.current_directory = ""  # Store current directory path
        self.pdf_window = None  # PDF viewer window
        self.create_widgets()

    def create_widgets(self):
        self.text_box = tk.Text(self.root, height=1, width=117)
        self.text_box.place(x=10, y=10)
        
        self.text_display = tk.Text(self.root, height=20, width=117, state='normal', cursor='hand2')
        self.text_display.place(x=10, y=65)
        
        self.text_display.bind('<Button-1>', self.on_file_click)
        
        self.submit_button = tk.Button(self.root, text="Open Directory", command=self.process_text)
        self.submit_button.place(x=11, y=35)
        
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_content)
        self.clear_button.place(x=105, y=35)
        
        self.update_name_button = tk.Button(self.root, text="Update Name", command=self.update_name)
        self.update_name_button.place (x=146, y=35)

        self.current_name_box = tk.Text(self.root, height=1, width=117, state='normal')
        self.current_name_box.place (x=10, y=520)

        # Image display label - FIXED: Use Canvas instead of Label
        self.canvas = tk.Canvas(self.root, bg="#6D6D6D", width=960, height=1080)
        self.canvas.place(x=960, y=0)
        
        # Prevent Enter from creating line breaks in text_box AND trigger submit
        self.text_box.bind('<Return>', lambda event: self.process_text() or "break")
        self.current_name_box.bind('<Return>', lambda event: self.update_name() or "break")

    def update_name(self):
        # need to update file names
        new_filename = self.current_name_box.get("1.0", tk.END).strip()
        self.new_file = os.path.join(self.current_directory, new_filename)
        os.rename(self.old_file, self.new_file)
        self.process_text()

    def clear_content(self):
        self.text_box.delete('1.0', tk.END)

    def process_text(self):
        user_input = self.text_box.get("1.0", tk.END).strip()
        print(user_input)
        self.current_directory = user_input  # Store the directory path
        
        self.text_display.config(state='normal')
        self.text_display.delete('1.0', tk.END)
        
        try:
            file_list = os.listdir(user_input)
            if not file_list:
                self.text_display.insert(tk.END, "No files found in this directory")
            else:
                for filename in file_list:
                    self.text_display.insert(tk.END, filename + "\n")
        except:
            self.text_display.insert(tk.END, "Not a proper directory path")

    def on_file_click(self, event):
        # Get the line that was clicked
        index = self.text_display.index(tk.CURRENT)
        line_start = index.split('.')[0] + '.0'
        line_end = index.split('.')[0] + '.end'
        
        # Get the filename from the clicked line
        filename = self.text_display.get(line_start, line_end).strip()
        
        if filename and self.current_directory:
            full_path = os.path.join(self.current_directory, filename)
            self.current_name_box.delete('1.0',tk.END)
            self.current_name_box.insert(tk.END, filename)
            self.old_file = full_path  # Store the full path of the clicked file
            self.display_pdf(full_path)

    def display_pdf(self, pdf_path):  # FIXED: Added pdf_path parameter
        try:
            # FIXED: Use the passed pdf_path instead of hardcoded PDF_PATH
            pdf_document = fitz.open(pdf_path)
            page = pdf_document[0]
            
            # FIXED: Correct method name
            pix = page.get_pixmap()
            
            # FIXED: Variable name typo
            img_data = pix.tobytes("ppm")
            pil_image = Image.open(io.BytesIO(img_data))
            
            # FIXED: Correct variable assignment and usage
            self.tk_image = ImageTk.PhotoImage(pil_image)
            
            # FIXED: Clear canvas and display image
            self.canvas.delete("all")
            self.canvas.create_image(10, 10, anchor=tk.NW, image=self.tk_image)
            
            pdf_document.close()
            
        except Exception as e:
            print(f"Failed to display PDF: {str(e)}")

root = tk.Tk()
JuicyAdventureApp(root)
root.mainloop()