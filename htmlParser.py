from html.parser import HTMLParser
import converter 
import csv
import os
from datetime import datetime, timedelta

class OnlySenderInFile(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"

class MessagesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.entries = []
        
    def handle_starttag(self, tag, attrs):
        for attr, value in attrs:
            if attr == "entry":
                timestamp, sender, receiver, chat_group, text = value.split(";;")
                self.entries.append(
                    {"Timestamp":timestamp,
                    "Sender":sender,
                    "Receiver": receiver, 
                    "ChatGroup": chat_group,
                    "Text": text})
            if attr == "haschecked":  
                self.entries[-1]["Remove"] = value

def get_csv(filename:str):
    with open(filename,'r',encoding='utf-8') as file:
        parse = MessagesParser()
        parse.feed(file.read())
        
    filename = os.path.basename(filename)
    with open(f"reviewed_data/{filename[:-5]}.csv", "w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["Timestamp","Sender","Receiver","ChatGroup","Text","Remove"]
        writer = csv.DictWriter(csv_file,fieldnames)
        writer.writeheader()
        writer.writerows(parse.entries)
    print(f"Saved: reviewed_data/{filename[:-5]}.csv")
    
# get_csv("message_html/WorkChat_2024-01-29.html")
def generate_reviewed_csvs(foldername:str):
    converter.create_folder("reviewed_data")
    for root, dirs, files in os.walk(foldername):
        for file in files:
            try:
                get_csv(os.path.join(root, file))
                
            except:
                print(f"Format Issue , File: {os.path.join(root, file)}")
                
# generate_reviewed_csvs("message_html")

def clean_data(foldername:str, output_name:str="compiled_data.csv", date_format:str = "%Y-%m-%d %H:%M:%S"):
    output_folder = "compiled_data"
    converter.create_folder(output_folder)
    output_file = f"{output_folder}\\{output_name}"
    fieldnames = ["Timestamp","Sender","Receiver","ChatGroup","Text","Remove"]
    with open(output_file,mode="w", encoding="utf-8") as output_csv:
        writer = csv.writer(output_csv,lineterminator="\n")
        writer.writerow(fieldnames)
        for root, dirs, files in os.walk(foldername):
            for file in files:
                path = os.path.join(root, file) 
                with open(path, mode='r',newline="", encoding='utf-8') as read_csv:
                    reader = csv.reader(read_csv)
                    next(reader)
                    for row in reader:
                        writer.writerow(row)
                
    sort_data(f"{output_folder}/{output_name}",date_format)
                        
def sort_data(filename:str, date_format:str):
    
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Extract header
        sorted_rows = sorted(reader, key=lambda row: datetime.strptime(str(row[0]),date_format) ) # Sort by second column (index 1)


    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write header
        writer.writerows(sorted_rows)  # Write sorted rows
    
    print(f"Saved: {filename}")