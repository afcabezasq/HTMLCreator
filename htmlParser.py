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
        self.target_class = ["message","message-bubble"]
        self.group_chat = [""]
        self.capture_data = False
        self.extracted_data = {0:[]}
        self.index = -1
        self.current_tag = ""
        self.people = []
        
    def handle_starttag(self, tag, attrs):
        for attr, value in attrs:
            classes_inside = [clss in value.split() for clss in self.target_class ]
            if attr == "class" and any(classes_inside):
                if "message" in value.split():
                    self.index += 1
                self.capture_data = True
            if attr == "people":
                people = value.split(";;")
                self.people.append(people[0])
                self.people.append(people[1])
                
        
        if tag == "h2":
            self.current_tag = "title"

        if tag == 'input':
            for attr, value in attrs:
                if attr == "haschecked":
                    self.extracted_data[self.index].append(f"Remove:{value}")

    def handle_data(self, data):
        if self.index not in self.extracted_data:
            self.extracted_data[self.index] = [] 
        if self.capture_data:
            data_to_add = data.strip()
            if  data_to_add != "":
                self.extracted_data[self.index].append(data_to_add)
        if self.current_tag == "title":
            self.extracted_data["Chat Group"]= data.strip()

            
    def handle_endtag(self, tag):
        self.capture_data = False
        if tag == "h2":
            self.current_tag = ""

def get_csv(filename:str):
    data = []
    senders = set()
    senders_values = []
    with open(filename,'r',encoding='utf-8') as file:
        parse = MessagesParser()
        parse.feed(file.read())
        table = parse.extracted_data
        del table[-1]
        chat_group = parse.extracted_data["Chat Group"].split(" - ")[0]
        for i in range(parse.index + 1):
            if(len(parse.extracted_data[i]) < 3):
                raise Exception(f"Format Problem with file {filename}")
            elif len(parse.extracted_data[i]) > 3:
                print(f"Entry size: {len(parse.extracted_data[i])}")
            send_date = parse.extracted_data[i][0]
            message = parse.extracted_data[i][1]
            remove_flag = parse.extracted_data[i][2]
            # send_date, message, remove_flag = parse.extracted_data[i]
            
            sender_date = send_date.split(" - ")
            sender, date = sender_date
            value_flag = remove_flag.split(":")[1]
            # print(f"Date: f{date}", f"Remove Flag: {value_flag}")
            
            if sender not in senders:
                senders.add(sender)
                senders_values.append(sender)

            data.append({
                "Timestamp":date,
                "Sender":sender,
                "ChatGroup": chat_group,
                "Text": message,
                "Remove": value_flag
            })
        # print(f"Number of senders: {len(senders_values)}", )
        if len(senders_values) < 2:
            if len(parse.people)<2:
                raise OnlySenderInFile(f"File does not contain receiver, Date:{date}, Chat Group:{chat_group}",error_code=2)
        if len(senders_values) == 2:
            for d in data:
                if d["Sender"] == senders_values[0]:
                    d["Receiver"] = senders_values[1]
                else:
                    d["Receiver"] = senders_values[0]
        if len(parse.people) == 2:
            for d in data:
                if d["Sender"] == parse.people[0]:
                    d["Receiver"] = parse.people[1]
                else:
                    d["Receiver"] = parse.people[0]
    
    filename = os.path.basename(filename)
    with open(f"reviewed_data/{filename[:-5]}.csv", "w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["Timestamp","Sender","Receiver","ChatGroup","Text","Remove"]
        writer = csv.DictWriter(csv_file,fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    
# get_csv("message_html/WorkChat_2024-01-29.html")
def generate_reviewed_csvs(foldername:str):
    converter.create_folder("reviewed_data")
    for root, dirs, files in os.walk(foldername):
        for file in files:
            try:
                get_csv(os.path.join(root, file))
            except OnlySenderInFile as e:
                print(f"Only sender in file: {e}, File: {os.path.join(root, file)}")
                
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
    