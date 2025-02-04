import tkinter as tk
from tkinter import filedialog, ttk
import csv

# Lista de colores para asignar a los interlocutores
colors = ["#1E90FF", "#32CD32", "#FFD700", "#FF69B4", "#A9A9A9", "#FF4500", "#00CED1", "#DAA520"]

# Diccionario para almacenar los colores asignados a cada interlocutor
interlocutor_colors = {}

# Diccionario para almacenar la posición (izquierda o derecha) asignada a cada interlocutor
interlocutor_positions = {}

# Lista para almacenar las variables de los checkbuttons
check_vars = []

def get_color_for_interlocutor(name):
    if name not in interlocutor_colors:
        # Asignar un color de la lista y repetir si hay más de 8 interlocutores
        color = colors[len(interlocutor_colors) % len(colors)]
        interlocutor_colors[name] = color
    return interlocutor_colors[name]

def get_position_for_interlocutor(name):
    if name not in interlocutor_positions:
        # Asignar la posición izquierda al primer interlocutor y derecha al resto
        position = 'left' if len(interlocutor_positions) == 0 else 'right'
        interlocutor_positions[name] = position
    return interlocutor_positions[name]

def open_csv_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        chats = list(reader)
        return chats

def display_chat_messages(parent, messages):
    for message in messages:
        # Obtener el color y la posición para el sender
        sender_color = get_color_for_interlocutor(message['Sender'])
        sender_position = get_position_for_interlocutor(message['Sender'])

        # Crear un frame para el mensaje
        frame = tk.Frame(parent, bg='white')
        frame.pack(pady=10, padx=10, fill='x')

        # Crear un frame para el globo de chat
        chat_frame = tk.Frame(frame, bg=sender_color, bd=2, relief='solid')
        chat_frame.pack(pady=5, padx=5, fill='x', expand=True, side=sender_position)

        # Crear un label para mostrar el contenido del mensaje
        label = tk.Label(chat_frame, text=message['Text'], bg=sender_color, fg='white', anchor='w', justify='left', wraplength=350)
        label.pack(pady=5, padx=5, fill='x', expand=True)

        # Crear un frame para el checkbutton y el texto "Remove"
        remove_frame = tk.Frame(frame, bg='white')
        remove_frame.pack(side='bottom', pady=5)

        # Crear un label para el texto "Remove"
        remove_label = tk.Label(remove_frame, text="Remove", bg='white', fg='black')
        remove_label.pack(side='left')

        # Crear un checkbutton debajo del label
        check_var = tk.BooleanVar()
        check_vars.append((check_var, message))
        check_button = tk.Checkbutton(remove_frame, variable=check_var, bg='white')
        check_button.pack(side='left')

def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir="./data", title="Select File", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
    
    if filename:
        # Limpiar la interfaz y las variables relacionadas
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        interlocutor_colors.clear()
        interlocutor_positions.clear()
        check_vars.clear()

        # Cargar y mostrar los nuevos mensajes
        chats = open_csv_file(filename)
        display_chat_messages(scrollable_frame, chats)

def remove_selected_messages():
    global filename
    if not filename:
        return

    # Leer el archivo CSV
    chats = open_csv_file(filename)

    # Filtrar los mensajes que no están seleccionados
    remaining_chats = [chat for var, chat in check_vars if not var.get()]

    # Sobrescribir el archivo CSV con los mensajes no seleccionados
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = chats[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(remaining_chats)

    # Limpiar la interfaz y volver a cargar los mensajes
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    check_vars.clear()
    display_chat_messages(scrollable_frame, remaining_chats)

# Crear la ventana principal
window = tk.Tk()
window.title('Chat Viewer')
window.geometry("600x800")
window.config(background="white")

# Crear un frame principal para contener los mensajes con un canvas y scrollbar
main_frame = tk.Frame(window, bg='white')
main_frame.pack(fill='both', expand=True)

canvas = tk.Canvas(main_frame, bg='white')
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg='white')

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Crear un frame para los botones
button_frame = tk.Frame(window, bg='white')
button_frame.pack(pady=10)

# Crear un botón para explorar archivos
button_explore = ttk.Button(button_frame, text="Browse Files", command=browseFiles)
button_explore.pack(side='left', padx=5)

# Crear un botón para eliminar los mensajes seleccionados
button_remove = ttk.Button(button_frame, text="Remove Selected Messages", command=remove_selected_messages)
button_remove.pack(side='left', padx=5)

# Iniciar el bucle principal de la aplicación
window.mainloop()