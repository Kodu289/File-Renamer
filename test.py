import tkinter as tk
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import io

# Your PDF file path
PDF_PATH = r"F:\Python Projects\PDF Reader\sample pdfs\file-example_PDF_1MB.pdf"

class SimplePDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer")
        self.root.configure(bg='#2d2d2d')
        
        # Create canvas
        self.canvas = tk.Canvas(root, bg='#3c3c3c', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load and display PDF
        self.load_pdf()
    
    def load_pdf(self):
        try:
            # Open PDF
            pdf_document = fitz.open(PDF_PATH)
            
            # Get first page (index 0)
            page = pdf_document[0]
            
            # Render page to pixmap
            pix = page.get_pixmap()
            
            # Convert to PIL Image
            img_data = pix.tobytes("ppm")
            pil_image = Image.open(io.BytesIO(img_data))
            
            # Convert to PhotoImage for Tkinter
            self.tk_image = ImageTk.PhotoImage(pil_image)
            
            # Display image on canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            
            # Update canvas scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Close PDF document
            pdf_document.close()
            
            print("PDF loaded successfully!")
            
        except Exception as e:
            print(f"Error loading PDF: {str(e)}")
            # Display error message on canvas
            self.canvas.create_text(400, 300, text=f"Error: {str(e)}", 
                                  fill='white', font=('Arial', 12))

def main():
    root = tk.Tk()
    root.geometry("800x600")
    
    app = SimplePDFViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()