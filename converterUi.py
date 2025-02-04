import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from converter import generate_html, read_csv

def browseFiles():
    filename = filedialog.askopenfilename(initialdir="./",title="Select File", filetypes=(("Text files",
                                                        "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
    
    g = read_csv(filename,date_format=selected_format.get())
    generate_html(g,date_format=selected_format.get())
    label_file_explorer.configure(text="HTML Files Generated")
    
    
window = tk.Tk()
# Set window title
window.title("Crowell's HTML Files Generator")
window.iconbitmap('./img/favicon.ico')
  
# Set window size
window.geometry("350x150")
  
#Set window background color
window.config(background = "white")
  
# Create a File Explorer label
label_file_explorer = tk.Label(window, 
                            text = "Search Desired File",
                            width = 20, height = 4, 
                            fg = "blue")
label_select_format = tk.Label(window, 
                            text = "Select Date Format",
                            width = 20, height = 4, 
                            fg = "blue")
      
button_explore = tk.Button(window, 
                        text = "Browse Files",
                        command = browseFiles) 
  
button_exit = tk.Button(window, 
                     text = "Exit",
                     command = exit) 
  
# Grid method is chosen for placing
# the widgets at respective positions 
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 1)
  
button_explore.grid(column = 1, row = 2)
label_select_format.grid(column = 0, row = 1)
  

selected_format = tk.StringVar()

formats =(("YYYY-MM-DD HH:MM:SS","%Y-%m-%d %H:%M:%S"),
          ("YYYY/MM/DD HH:MM:SS","%Y/%m/%d %H:%M:%S"),
          ("MM/DD/YYYY HH:MM:SS AM/PM","%m/%d/%Y %I:%M:%S %p"))

row = 2
for text, format in formats:
    r = ttk.Radiobutton(window,text=text,value=format, variable=selected_format)
    r.grid(column=0,row=row)
    row += 1
  
# Let the window wait for any events
window.mainloop()
