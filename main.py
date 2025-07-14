from PIL import Image, ImageTk
import tkinter as tk
import os
import fitz  # PyMuPDF
import io

# Make it so that if the word is in a () it still gets captilized

# create a sub panel where it shows the MB file size of each respective file and see if they match
# add a page counter

###### create a button that lets me instantly remove a certain word from the multiple highlighted files only


class File_Renamer:
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
        self.text_box = tk.Text(self.root, height=2, width=90, bg="#E0E0E0")
        self.text_box.place(x=200+950, y=10)
        
        self.text_display = tk.Text(self.root, height=52, width=117, state='normal', cursor='hand2', bg="#E0E0E0")
        self.text_display.place(x=10+950, y=150)
        self.text_display.bind('<Button-1>', self.on_file_click)
        
        self.submit_button = tk.Button(self.root, text="Open Directory", command=self.process_text)
        self.submit_button.place(x=11+950, y=65)
        
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_content)
        self.clear_button.place(x=105+950, y=65)
        
        self.update_name_button = tk.Button(self.root, text="Update Name", command=self.update_name)
        self.update_name_button.place (x=146+950, y=65)

        self.format_button = tk.Button(self.root, text="Format", command=self.basic_format)
        self.format_button.place (x=240+950, y=65)

        self.format_button = tk.Button(self.root, text="Delete", command=self.delete)
        self.format_button.place (x=310+950, y=65)

        self.format_button = tk.Button(self.root, text="Legal", command=self.legal)
        self.format_button.place (x=390+950, y=65)
        self.format_button = tk.Button(self.root, text="General", command=self.general)
        self.format_button.place (x=430+950, y=65)

        self.current_name_box = tk.Text(self.root, height=2, width=117, state='normal', bg="#E0E0E0")
        self.current_name_box.place (x=10+950, y=95)

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
    
    def legal(self):
        self.input_wait = self.text_box.get("1.0", tk.END).strip()
        user_input = rf"C:\Users\LinH\OneDrive - BGIS\Documents - BGIS - Infrastructure Ontario Lease Document Portal\IO - Lease Admin Document Repository\{self.input_wait}\legal"
        print(user_input)
        self.current_directory = user_input  # Store the directory path
        self.text_display.config(state='normal')
        self.text_display.delete('1.0', tk.END)
        try:
            # Always update file_list and last_directory
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
        
        self.last_folder = "legal"
    
    def general(self):
        self.input_wait = self.text_box.get("1.0", tk.END).strip()
        user_input = rf"C:\Users\LinH\OneDrive - BGIS\Documents - BGIS - Infrastructure Ontario Lease Document Portal\IO - Lease Admin Document Repository\{self.input_wait}\general"
        print(user_input)
        self.current_directory = user_input  # Store the directory path
        self.text_display.config(state='normal')
        self.text_display.delete('1.0', tk.END)
        try:
            # Always update file_list and last_directory
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

        self.last_folder = "general"

    def delete(self):
        if self.current_pdf_path:
            try:
                os.remove(self.current_pdf_path)
                print(f"Deleted: {self.current_pdf_path}")
                # Remove from file_list and update display
                filename = os.path.basename(self.current_pdf_path)
                self.file_list.remove(filename)
                self.text_display.config(state='normal')
                self.text_display.delete('1.0', tk.END)
                for fname in self.file_list:
                    if fname.lower().endswith('.pdf'):
                        display_name = fname[:-4]
                    else:
                        display_name = fname
                    self.text_display.insert(tk.END, display_name + "\n")
                self.text_display.config(state='disabled')
                # Reset current PDF path and page
                self.current_pdf_path = None
                self.current_page = 0
            except Exception as e:
                print(f"Error deleting file: {str(e)}")

    def basic_format(self):
        for filename in os.listdir(self.current_directory):
            if filename.endswith(".pdf"):
                # Start with the original filename
                new_filename = filename

                # 1. Add prefix if needed
                if filename[:6] != self.input_wait:
                    new_filename = self.input_wait + " " + new_filename

                # 4. Capitalize words (with exception for words after '(')
                small_words = {'and', 'the', 'of', 'in', 'to', 'for','a','an', 'is', 'on', 'at', 'by', 'with', 'as', 'this', 'that'}
                words = new_filename.split()
                result = []
                prev_word = ""
                for i, word in enumerate(words):
                    # Capitalize if previous word ends with '('
                    if prev_word.endswith('('):
                        result.append(word.capitalize())
                    # Capitalize if word starts with '(' (e.g., (apple) -> (Apple))
                    elif word.startswith('(') and len(word) > 1:
                        result.append('(' + word[1].upper() + word[2:])
                    elif i == 0 or word.lower() not in small_words:
                        result.append(word.capitalize())
                    else:
                        result.append(word.lower())
                    prev_word = word
                new_filename = ' '.join(result)

                # 2. Apply replacements
                replacements = [
                    ("_", " "),
                    ("-", " "),
                    ("Second ", "2nd "),
                    ("First ", "1st "),
                    ("Third ", "3rd "),
                    ('Ti', 'TI'),
                    ("Transaction Summary Approval Form", "Transaction Summary and Approval Form"),
                    ('Transaction Summary Form','Transaction Summary and Approval Form'),
                    ('Transaction Summary and Approval Forms','Transaction Summary and Approval Form'),
                    ("Leaa", "Lease Extension and Amending Agreement"),
                    ("Sect ", "Section "),
                    ("Sec ", "Section "),
                    ("Tsf Taf", "Transaction Summary and Approval Form"),
                    ("&", "and"),
                    ("Pm ", "PM "),
                    ("Io ", "IO "),
                    ("Cbre","CBRE"),
                    ("Bgis", "BGIS"),
                    ("Lanlord", "Landlord"),
                    ("Section28", "Section 28"),
                    ("Notice and Direction", "Notice of Direction"),
                    ("Direction and Notice", "Notice of Direction"),
                    ("Notification", "Notice"),
                    ("Forms", "Form"),

                    # Above is standard change
                    # bottom is quick name change

                    (" Loi ", " Letter of Intent "),
                    (" Ta ", " Tenant Acknowledement "),
                    (" Nod ", " Notice of Direction "),
                    (" I28 ", " IO Section 28 Memo "),
                    (" Ec ", " Email Correspondence "),
                    (" Tsf ", " Transaction Summary and Approval Form "),
                    (" Ote ", " Option to Extend Letter "),
                    (" F1 ", " Form 1 "),
                    (" Yea ", " Year End Adjustment "),
                    (" Coi ", " Certificate of Insurance "),
                    (" Rf ", " Reminder for "),
                ]
                for old, new in replacements:
                    new_filename = new_filename.replace(old, new)

                # 3. Remove excess spaces
                new_filename = ' '.join(new_filename.split())

                # 5. Only rename if the name has changed
                old_filepath = os.path.join(self.current_directory, filename)
                new_filepath = os.path.join(self.current_directory, new_filename)
                if old_filepath != new_filepath:
                    try:
                        os.rename(old_filepath, new_filepath)
                        print(f"Renamed: {filename} -> {new_filename}")
                    except Exception as e:
                        print(f"Error renaming file {filename}: {str(e)}")

        if self.last_folder == "legal":
            self.legal()
        elif self.last_folder == "general":
            self.general()
        else:
            print('defaulting to nothing')

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
        self.input_wait = self.text_box.get("1.0", tk.END).strip()
        user_input = rf"C:\Users\LinH\OneDrive - BGIS\Documents - BGIS - Infrastructure Ontario Lease Document Portal\IO - Lease Admin Document Repository\{self.input_wait}"
        print(user_input)
        self.current_directory = user_input  # Store the directory path
        self.text_display.config(state='normal')
        self.text_display.delete('1.0', tk.END)
        try:
            # Always update file_list and last_directory
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
File_Renamer(root)
root.mainloop()