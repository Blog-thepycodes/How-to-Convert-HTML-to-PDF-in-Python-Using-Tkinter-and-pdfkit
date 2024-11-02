import tkinter as tk
from tkinter import filedialog, messagebox
import pdfkit
import threading
import validators  


# Configure path to wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')# This is my file path to wkhtmltopdf\bin\wkhtmltopdf.exe so be sure to put your own 


# Define custom options for better webpage capturing
options = {
   'page-size': 'A4',
   'margin-top': '0.75in',
   'margin-right': '0.75in',
   'margin-bottom': '0.75in',
   'margin-left': '0.75in',
   'encoding': "UTF-8",
   'no-outline': None,
   'javascript-delay': 5000,  # Wait 5 seconds for JavaScript to load
   'no-background': False,
   'disable-smart-shrinking': True,
}




# Function to convert HTML to PDF
def convert_to_pdf():
   content = text_input.get("1.0", tk.END).strip()
   pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])


   if not pdf_path:
       return  # Exit if no file is chosen


   try:
       loading_label.config(text="Converting to PDF...")
       root.update_idletasks()  # Refresh GUI to show loading message


       # Check selected input type and convert
       if var.get() == "html_string":
           pdfkit.from_string(content, pdf_path, configuration=config, options=options)
       elif var.get() == "html_file":
           pdfkit.from_file(content, pdf_path, configuration=config, options=options)
       elif var.get() == "url":
           if not validators.url(content):
               raise ValueError("Invalid URL")
           pdfkit.from_url(content, pdf_path, configuration=config, options=options)


       messagebox.showinfo("Success", "PDF created successfully!")
   except Exception as e:
       messagebox.showerror("Error", f"An error occurred: {e}")
   finally:
       loading_label.config(text="")  # Clear loading message




# Function to open file dialog for HTML file selection
def select_file():
   file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
   if file_path:
       text_input.delete("1.0", tk.END)
       text_input.insert(tk.END, file_path)




# Function to start PDF conversion in a separate thread
def start_conversion():
   threading.Thread(target=convert_to_pdf).start()




# Set up the main window
root = tk.Tk()
root.title("HTML to PDF Converter - The Pycodes")
root.geometry("500x450")


# Frame for radio buttons
input_type_frame = tk.LabelFrame(root, text="Choose Input Type", padx=10, pady=10)
input_type_frame.pack(padx=10, pady=5, fill="x")


var = tk.StringVar(value="html_string")
tk.Radiobutton(input_type_frame, text="HTML String", variable=var, value="html_string").pack(anchor="w", padx=10,
                                                                                            pady=2)
tk.Radiobutton(input_type_frame, text="HTML File Path", variable=var, value="html_file", command=select_file).pack(
   anchor="w", padx=10, pady=2)
tk.Radiobutton(input_type_frame, text="URL", variable=var, value="url").pack(anchor="w", padx=10, pady=2)


# Text widget for HTML input
text_frame = tk.LabelFrame(root, text="HTML Content or Path/URL", padx=10, pady=10)
text_frame.pack(padx=10, pady=5, fill="both", expand=True)
text_input = tk.Text(text_frame, wrap="word", height=10)
text_input.pack(fill="both", expand=True)


# Convert button and loading indicator
convert_button = tk.Button(root, text="Convert to PDF", command=start_conversion)
convert_button.pack(pady=10)
loading_label = tk.Label(root, text="", fg="blue")
loading_label.pack()


root.mainloop()
