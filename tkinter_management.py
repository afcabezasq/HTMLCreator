import tkinter as tk
from tkinter import ttk

def display_message(parent, message):
    # Crear un frame para el mensaje
    frame = tk.Frame(parent, bg='white')
    frame.pack(pady=10, padx=10, fill='x')

    # Crear un frame para el globo de chat
    chat_frame = tk.Frame(frame, bg='lightblue', bd=2, relief='solid')
    chat_frame.pack(pady=5, padx=5, fill='x', expand=True)

    # Crear un label para mostrar el contenido del mensaje
    label = tk.Label(chat_frame, text=message['Text'], bg='lightblue', anchor='w', justify='left', wraplength=350)
    label.pack(pady=5, padx=5, fill='x', expand=True)

    # Crear un checkbutton debajo del label
    check_var = tk.BooleanVar()
    check_button = tk.Checkbutton(frame, text="Select", variable=check_var, bg='white')
    check_button.pack(side='bottom', pady=5)
