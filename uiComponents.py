import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from converter import read_csv, generate_html
from htmlParser import generate_reviewed_csvs, clean_data

DATE_FORMATS = (("YYYY-MM-DD HH:MM:SS","%Y-%m-%d %H:%M:%S"),
          ("YYYY/MM/DD HH:MM:SS","%Y/%m/%d %H:%M:%S"),
          ("MM/DD/YYYY HH:MM:SS AM/PM","%m/%d/%Y %I:%M:%S %p"))

# class ScrollableFrame(ttk.Frame):
#     def __init__(self, container):
#         super().__init__(container)
#         self.canvas = tk.Canvas(self)
#         scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
#         self.scrollable_frame = ttk.Frame(self.canvas)
#         self.scrollable_frame.bind(
#             "<Configure>",
#             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#         )
#         self.canvas.create_window((0,0), window=self.scrollable_frame,anchor="nw")
#         self.canvas.configure(yscrollcommand=scrollbar.set)
#         self.canvas.pack(side="left", fill="both", expand=True)
#         scrollbar.pack(side="right",fill="y")
        
#     def get_frame(self):
#         return self.scrollable_frame
    
#     def get_canvas(self):
#         return self.canvas


        
class SelectDateFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container, width=600)
        self.select_date_label = self.label_select_date = tk.Label(self, 
                    text="Select Date Format",
                    fg = "blue")
        self.select_date_label.pack(side="top")
        
        self.selected_format = tk.StringVar()
        
        for text, format in DATE_FORMATS:
            r = ttk.Radiobutton(self,text=text,value=format, variable=self.selected_format)
            r.pack(side="top",anchor="w")
        

class FileExplorerFrame(ttk.Frame):
    def __init__(self, container, date_format_frame: SelectDateFrame):
        self.date_format_frame = date_format_frame
        super().__init__(container)
        self.label_file_explorer = tk.Label(self, 
                    text="Search Desired File",
                    fg = "blue")
        self.label_file_explorer.pack(side="top",anchor="n")
        self.file_explorer_button = tk.Button(self,text = "Browse Files",
                        command = self.browseFiles)
        self.file_explorer_button.pack(side="top", anchor="n")
        
    def browseFiles(self):
        dateFormat = self.date_format_frame.selected_format.get()
        filename = filedialog.askopenfilename(initialdir="./",title="Select File", filetypes=(("Text files",
                                                        "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
        g = read_csv(filename,date_format=dateFormat)
        generate_html(g,date_format=dateFormat)
        self.label_file_explorer.configure(text="HTML Files Generated")
        
class SearchHTMLFrame(ttk.Frame):
    def __init__(self, container):
        
        super().__init__(container,)
        self.label_file_explorer = tk.Label(self, 
                    text="Search HTML Revied Files",
                    fg = "blue")
        self.label_file_explorer.pack(side="top")
        self.file_explorer_button = tk.Button(self,text = "Browse HTML files folder",
                        command = self.browseFiles)
        self.file_explorer_button.pack(side="top")
        
    def browseFiles(self):
        foldername = filedialog.askdirectory(initialdir="./",title="Select Folder")
        generate_reviewed_csvs(foldername)
        clean_data(foldername)
        self.label_file_explorer.configure(text="Cleaned data")
        
class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.style = ttk.Style()
        self.style.configure("TFrame", background="white")
        self.top_frame = ttk.Frame(self,width=800,height=100,style="TFrame")
        self.top_frame.pack(side="top")
        self.select_date_frame = SelectDateFrame(self.top_frame)
        self.file_explorer_frame = FileExplorerFrame(self.top_frame,self.select_date_frame)
        self.select_date_frame.pack(side="left",padx=30,anchor="w")
        self.file_explorer_frame.pack(side="right",padx=30, anchor="ne")
        self.reviewed_data = ttk.Frame(self)
        self.reviewed_data.pack(side="top",pady = 30, anchor="center")
        self.searchHtmlFiles = SearchHTMLFrame(self.reviewed_data)
        self.searchHtmlFiles.pack(side="top",anchor="center")
        
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.config(background = "white")
        scrollable_frame = MainFrame(self)
        scrollable_frame.pack(fill="both",expand=True)
        
    def setTitle(self,title:str):
        self.title(title)
        
    def setSize(self,geometry:str):
        self.geometry(geometry)
        
    def runApp(self, title, size):
        self.setTitle(title)
        self.setSize(size)
        self.mainloop()
        

    