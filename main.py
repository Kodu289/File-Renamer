from PIL import Image, ImageTk
import tkinter as tk
import os
import fitz  # PyMuPDF
import io

class JuicyAdventureApp:
    def __init__(self, root):
        self.root = root
        root.geometry("1920x1080")
        root.configure(bg="#B4B4B4")
        root.title("File Renamer")
        
        self.current_directory = ""  # Store current directory path
        self.pdf_window = None  # PDF viewer window
        self.current_pdf_path = None  # Track current PDF path
        self.current_page = 0         # Track current page number
        self.total_pages = 0          # Track total pages in current PDF
        self.zoom = 1.16  # Default zoom level
        self.create_widgets()

    def create_widgets(self):
        self.text_box = tk.Text(self.root, height=1, width=117, bg="#E0E0E0")
        self.text_box.place(x=10+950, y=10)
        
        self.text_display = tk.Text(self.root, height=40, width=117, state='normal', cursor='hand2', bg="#E0E0E0")
        self.text_display.place(x=10+950, y=90)
        self.text_display.bind('<Button-1>', self.on_file_click)
        
        self.submit_button = tk.Button(self.root, text="Open Directory", command=self.process_text)
        self.submit_button.place(x=11+950, y=35)

        self.submit2_button = tk.Button(self.root, text="Open Directory2", command=self.process_text)
        self.submit2_button.place(x=260+950, y=35)
        
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_content)
        self.clear_button.place(x=105+950, y=35)
        
        self.update_name_button = tk.Button(self.root, text="Update Name", command=self.update_name)
        self.update_name_button.place (x=146+950, y=35)

        self.current_name_box = tk.Text(self.root, height=1, width=117, state='normal', bg="#E0E0E0")
        self.current_name_box.place (x=10+950, y=65)

        # Image display label - FIXED: Use Canvas instead of Label
        # Lower the canvas so it doesn't cover the buttons
        self.canvas = tk.Canvas(self.root, bg="#6D6D6D", width=940, height=1080)
        self.canvas.place(x=960-950, y=10)
        # Bind mouse wheel to zoom in/out when hovering over the canvas
        self.canvas.bind('<MouseWheel>', self.on_canvas_scroll)
        
        # Prevent Enter from creating line breaks in text_box AND trigger submit
        self.text_box.bind('<Return>', lambda event: self.process_text() or "break")
        self.current_name_box.bind('<Return>', lambda event: self.update_name() or "break")
        # Bind left/right arrow keys to previous/next page

    def next_page(self):
        if self.current_pdf_path and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_pdf(self.current_pdf_path, self.current_page)

    def previous_page(self):
        if self.current_pdf_path and self.current_page > 0:
            self.current_page -= 1
            self.display_pdf(self.current_pdf_path, self.current_page)

    def update_name(self):
        new_display_name = self.current_name_box.get("1.0", tk.END).strip()
        new_filename = new_display_name + ".pdf"
        self.new_file = os.path.join(self.current_directory, new_filename)
        os.rename(self.old_file, self.new_file)
        # Update file_list in place
        old_name = os.path.basename(self.old_file)
        for i, fname in enumerate(self.file_list):
            if fname == old_name:
                self.file_list[i] = new_filename
                break
        # After renaming, refresh the list and move highlight to next file
        self.text_display.config(state='normal')
        self.text_display.delete('1.0', tk.END)
        self.display_name_map = {}
        for filename in self.file_list:
            if filename.lower().endswith('.pdf'):
                display_name = filename[:-4]
            else:
                display_name = filename
            self.display_name_map[display_name] = filename
            self.text_display.insert(tk.END, display_name + "\n")
        self.text_display.config(state='disabled')
        # Find the current highlighted line
        lines = self.text_display.get('1.0', tk.END).splitlines()
        try:
            current_index = lines.index(new_display_name)
        except ValueError:
            current_index = -1
        next_index = current_index + 1
        if 0 <= next_index < len(lines):
            line_start = f"{next_index+1}.0"
            line_end = f"{next_index+1}.end"
            self.text_display.tag_remove('highlight', '1.0', tk.END)
            self.text_display.tag_add('highlight', line_start, line_end)
            self.text_display.tag_config('highlight', background='#3399FF', foreground='white')
            display_name = lines[next_index].strip()
            filename = self.display_name_map.get(display_name, display_name)
            if filename and self.current_directory:
                full_path = os.path.join(self.current_directory, filename)
                self.current_name_box.delete('1.0',tk.END)
                self.current_name_box.insert(tk.END, display_name)
                self.old_file = full_path
                self.current_pdf_path = full_path
                self.current_page = 0
                try:
                    with fitz.open(full_path) as pdf_document:
                        self.total_pages = pdf_document.page_count
                except Exception:
                    self.total_pages = 0
                self.display_pdf(full_path, 0)
            self.current_name_box.focus_set()

    def clear_content(self):
        self.text_box.delete('1.0', tk.END)

    def process_text(self):
        user_input = self.text_box.get("1.0", tk.END).strip()
        print(user_input)
        self.current_directory = user_input  # Store the directory path
        self.text_display.config(state='normal')
        self.text_display.delete('1.0', tk.END)
        try:
            # Only update file_list if it's empty or directory changed
            if not hasattr(self, 'file_list') or getattr(self, 'last_directory', None) != user_input:
                self.file_list = os.listdir(user_input)
                self.last_directory = user_input
            self.display_name_map = {}
            for filename in self.file_list:
                if filename.lower().endswith('.pdf'):
                    display_name = filename[:-4]
                else:
                    display_name = filename
                self.display_name_map[display_name] = filename
                self.text_display.insert(tk.END, display_name + "\n")
        except:
            self.text_display.insert(tk.END, "Not a proper directory path")
        self.text_display.config(state='disabled')

    def on_file_click(self, event):
        # Get the line that was clicked
        index = self.text_display.index(tk.CURRENT)
        line_num = index.split('.')[0]
        line_start = line_num + '.0'
        line_end = line_num + '.end'
        # Remove previous highlight
        self.text_display.tag_remove('highlight', '1.0', tk.END)
        # Highlight the clicked line in blue
        self.text_display.tag_add('highlight', line_start, line_end)
        self.text_display.tag_config('highlight', background='#3399FF', foreground='white')
        # Get the display name from the clicked line
        display_name = self.text_display.get(line_start, line_end).strip()
        # Map back to the real filename
        filename = self.display_name_map.get(display_name, display_name)
        if filename and self.current_directory:
            full_path = os.path.join(self.current_directory, filename)
            self.current_name_box.delete('1.0',tk.END)
            self.current_name_box.insert(tk.END, display_name)
            self.old_file = full_path  # Store the full path of the clicked file
            self.current_pdf_path = full_path  # Track current PDF
            self.current_page = 0  # Reset to first page
            try:
                with fitz.open(full_path) as pdf_document:
                    self.total_pages = pdf_document.page_count
            except Exception:
                self.total_pages = 0
            self.display_pdf(full_path, 0)
        # Move focus to the renaming text window after the click event is processed
        event.widget.after(1, lambda: self.current_name_box.focus_set())

    def zoom_in(self):
        self.zoom += 0.04
        if self.current_pdf_path:
            self.display_pdf(self.current_pdf_path, self.current_page)

    def zoom_out(self):
        self.zoom = max(0.04, self.zoom - 0.04)
        if self.current_pdf_path:
            self.display_pdf(self.current_pdf_path, self.current_page)

    def on_canvas_scroll(self, event):
        # If Ctrl is held, zoom; otherwise, scroll pages
        if (event.state & 0x0004):  # 0x0004 is the mask for Ctrl on Windows
            if event.delta > 0:
                self.zoom_in()
            elif event.delta < 0:
                self.zoom_out()
        else:
            if event.delta > 0:
                self.previous_page()
            elif event.delta < 0:
                self.next_page()

    def display_pdf(self, pdf_path, page_number=0):
        try:
            pdf_document = fitz.open(pdf_path)
            if page_number < 0 or page_number >= pdf_document.page_count:
                page_number = 0
            page = pdf_document[page_number]
            # Use the current zoom level
            mat = fitz.Matrix(self.zoom, self.zoom)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("ppm")
            pil_image = Image.open(io.BytesIO(img_data))
            self.tk_image = ImageTk.PhotoImage(pil_image)
            self.canvas.delete("all")
            # Right-align the image
            canvas_width = int(self.canvas['width'])
            img_width = self.tk_image.width()
            x_pos = canvas_width - img_width if canvas_width > img_width else 0
            self.canvas.create_image(x_pos, 10, anchor=tk.NW, image=self.tk_image)
            pdf_document.close()
        except Exception as e:
            print(f"Failed to display PDF: {str(e)}")

root = tk.Tk()
JuicyAdventureApp(root)
root.mainloop()