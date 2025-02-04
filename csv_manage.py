import csv

def read_csv_file_s(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data
