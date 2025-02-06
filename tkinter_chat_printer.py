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
        # Agregar los campos 'removed', 'reviewed' e 'important' si no existen
        for chat in chats:
            if 'removed' not in chat:
                chat['removed'] = 'false'
            if 'reviewed' not in chat:
                chat['reviewed'] = 'false'
            if 'important' not in chat:
                chat['important'] = 'false'
        return chats

def save_csv_file(filepath, chats):
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        fieldnames = chats[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(chats)

def display_chat_messages(parent, messages):
    for message in messages:
        # Filtrar mensajes según el estado de 'removed', 'reviewed', 'important', la fecha seleccionada y el estado de los Checkbutton
        if not show_all_var.get() and message['removed'] == 'true':
            continue
        if not show_reviewed_var.get() and message['reviewed'] == 'true':
            continue
        if show_important_var.get() and message['important'] != 'true':
            continue
        if selected_date.get() and message['Timestamp'].split()[0] != selected_date.get():
            continue

        # Obtener el color y la posición para el sender
        sender_color = get_color_for_interlocutor(message['Sender'])
        sender_position = get_position_for_interlocutor(message['Sender'])

        # Crear un frame para el mensaje
        frame = tk.Frame(parent, bg='white')
        frame.pack(pady=10, padx=10, fill='x')

        # Crear un frame para el globo de chat con bordes suaves
        chat_frame = tk.Frame(frame, bg=sender_color, bd=2, relief='solid', padx=10, pady=10)
        chat_frame.pack(pady=5, padx=5, fill='x', expand=True, side=sender_position)

        # Crear un label para mostrar el contenido del mensaje
        label = tk.Label(chat_frame, text=message['Text'], bg=sender_color, fg='white', anchor='w', justify='left', wraplength=350)
        label.pack(pady=5, padx=5, fill='x', expand=True)

        # Crear un label para mostrar la fecha del mensaje
        date_label = tk.Label(chat_frame, text=message['Timestamp'], bg=sender_color, fg='white', anchor='w', justify='left', font=("Arial", 6))
        date_label.pack(pady=2, padx=5, fill='x', expand=True)

        # Crear un frame para los checkbuttons y los textos "Remove", "Reviewed" e "Important"
        check_frame = tk.Frame(frame, bg='white')
        check_frame.pack(side='bottom', pady=5)

        # Crear un frame para "Remove"
        remove_frame = tk.Frame(check_frame, bg='white')
        remove_frame.pack(side='top', pady=2)
        remove_label = tk.Label(remove_frame, text="Remove", bg='white', fg='black')
        remove_label.pack(side='left')
        remove_var = tk.BooleanVar(value=(message['removed'] == 'true'))
        check_vars.append((remove_var, message, 'removed'))
        remove_checkbutton = tk.Checkbutton(remove_frame, variable=remove_var, bg='white')
        remove_checkbutton.pack(side='left')

        # Crear un frame para "Reviewed"
        reviewed_frame = tk.Frame(check_frame, bg='white')
        reviewed_frame.pack(side='top', pady=2)
        reviewed_label = tk.Label(reviewed_frame, text="Reviewed", bg='white', fg='black')
        reviewed_label.pack(side='left')
        reviewed_var = tk.BooleanVar(value=(message['reviewed'] == 'true'))
        check_vars.append((reviewed_var, message, 'reviewed'))
        reviewed_checkbutton = tk.Checkbutton(reviewed_frame, variable=reviewed_var, bg='white')
        reviewed_checkbutton.pack(side='left')

        # Crear un frame para "Important"
        important_frame = tk.Frame(check_frame, bg='white')
        important_frame.pack(side='top', pady=2)
        important_label = tk.Label(important_frame, text="Important", bg='white', fg='black')
        important_label.pack(side='left')
        important_var = tk.BooleanVar(value=(message['important'] == 'true'))
        check_vars.append((important_var, message, 'important'))
        important_checkbutton = tk.Checkbutton(important_frame, variable=important_var, bg='white')
        important_checkbutton.pack(side='left')

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
        update_date_options(chats)
        display_chat_messages(scrollable_frame, chats)

def update_messages_status():
    global filename
    if not filename:
        return

    # Leer el archivo CSV
    chats = open_csv_file(filename)

    # Actualizar los campos 'removed', 'reviewed' e 'important' de los mensajes seleccionados
    for var, message, field in check_vars:
        # Encontrar el mensaje correspondiente en la lista chats y actualizarlo
        for chat in chats:
            if chat == message:
                chat[field] = 'true' if var.get() else 'false'
                break

    # Guardar los cambios en el archivo CSV
    save_csv_file(filename, chats)

    # Limpiar la interfaz y volver a cargar los mensajes
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    check_vars.clear()
    display_chat_messages(scrollable_frame, [chat for chat in chats if chat['removed'] == 'false' and chat['reviewed'] == 'false'])

def toggle_show_all():
    # Limpiar la interfaz y volver a cargar los mensajes según el estado de los Checkbutton
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    check_vars.clear()
    chats = open_csv_file(filename)
    display_chat_messages(scrollable_frame, chats)

def update_date_options(chats):
    # Obtener todas las fechas únicas de los mensajes
    dates = sorted(set(chat['Timestamp'].split()[0] for chat in chats))
    # Actualizar el OptionMenu con las fechas
    date_menu['menu'].delete(0, 'end')
    for date in dates:
        date_menu['menu'].add_command(label=date, command=tk._setit(selected_date, date, update_displayed_messages))
    # Establecer la fecha seleccionada a la primera fecha disponible
    if dates:
        selected_date.set(dates[0])
    else:
        selected_date.set('')

def update_displayed_messages(*args):
    # Limpiar la interfaz y volver a cargar los mensajes según la fecha seleccionada
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    check_vars.clear()
    chats = open_csv_file(filename)
    display_chat_messages(scrollable_frame, chats)

# Crear la ventana principal
window = tk.Tk()
window.title('Chat Viewer')
window.geometry("600x800")
window.config(background="white")

# Crear las variables show_all_var, show_reviewed_var y show_important_var después de crear la ventana principal
show_all_var = tk.BooleanVar(value=False)
show_reviewed_var = tk.BooleanVar(value=False)
show_important_var = tk.BooleanVar(value=False)

# Crear la variable selected_date después de crear la ventana principal
selected_date = tk.StringVar()
selected_date.trace_add('write', update_displayed_messages)

# Crear un frame para el OptionMenu de fechas
date_frame = tk.Frame(window, bg='white')
date_frame.pack(pady=10)

# Crear un OptionMenu para seleccionar la fecha
selected_date.set('')  # Valor inicial vacío
date_menu = tk.OptionMenu(date_frame, selected_date, '')
date_menu.pack(side='left', padx=5)

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

# Crear un botón para actualizar el estado de los mensajes
button_update = ttk.Button(button_frame, text="Update", command=update_messages_status)
button_update.pack(side='left', padx=5)

# Crear un frame para los Checkbutton y los Label
show_all_frame = tk.Frame(button_frame, bg='white')
show_all_frame.pack(side='left', padx=5)

# Crear un frame para "Show Removed Messages"
show_removed_frame = tk.Frame(show_all_frame, bg='white')
show_removed_frame.pack(side='top', pady=2)
show_all_label = tk.Label(show_removed_frame, text="Show Removed Messages", bg='white', fg='black')
show_all_label.pack(side='left')
show_all_checkbutton = tk.Checkbutton(show_removed_frame, variable=show_all_var, command=toggle_show_all, bg='white')
show_all_checkbutton.pack(side='left')

# Crear un frame para "Show Reviewed Messages"
show_reviewed_frame = tk.Frame(show_all_frame, bg='white')
show_reviewed_frame.pack(side='top', pady=2)
show_reviewed_label = tk.Label(show_reviewed_frame, text="Show Reviewed Messages", bg='white', fg='black')
show_reviewed_label.pack(side='left')
show_reviewed_checkbutton = tk.Checkbutton(show_reviewed_frame, variable=show_reviewed_var, command=toggle_show_all, bg='white')
show_reviewed_checkbutton.pack(side='left')

# Crear un frame para "Show Important Messages"
show_important_frame = tk.Frame(show_all_frame, bg='white')
show_important_frame.pack(side='top', pady=2)
show_important_label = tk.Label(show_important_frame, text="Show Important Messages", bg='white', fg='black')
show_important_label.pack(side='left')
show_important_checkbutton = tk.Checkbutton(show_important_frame, variable=show_important_var, command=toggle_show_all, bg='white')
show_important_checkbutton.pack(side='left')

# Iniciar el bucle principal de la aplicación
window.mainloop()