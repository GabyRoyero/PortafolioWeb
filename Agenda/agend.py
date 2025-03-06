import tkinter as tk
from database import insert, view, delete, update
from tkinter import ttk, messagebox
from datetime import datetime

# Ventana principal
win = tk.Tk()
win.geometry("800x400")
win.title("Agenda de Contactos")
win.configure(bg="#f0f0f0")  # Color de fondo claro

# Entradas y etiquetas
input_name = tk.Entry(win)
input_phone = tk.Entry(win)
label_name = tk.Label(win, text="Nombre", bg="#f0f0f0")
label_phone = tk.Label(win, text="Teléfono", bg="#f0f0f0")

# Barra de búsqueda
search_var = tk.StringVar()
search_entry = tk.Entry(win, textvariable=search_var, width=30)
search_label = tk.Label(win, text="Buscar", bg="#f0f0f0")

# Tabla Treeview para mostrar los contactos
agenda = ttk.Treeview(win, columns=("id", "name", "phone", "date"), show="headings")
agenda.heading("id", text="ID")
agenda.heading("name", text="NOMBRE")
agenda.heading("phone", text="TELÉFONO")
agenda.heading("date", text="FECHA")

# Ajustar las columnas
agenda.column("id", anchor="center")
agenda.column("name", anchor="center")
agenda.column("phone", anchor="center")
agenda.column("date", anchor="center")

contacts = view()  # Cargar los contactos desde la base de datos

# Función para añadir un contacto
def add():
    name = input_name.get().strip()
    phone = input_phone.get().strip()
    date = datetime.now().strftime("%Y-%m-%d")

    if not name or not phone:
        messagebox.showwarning("Campos Vacíos", "Por favor, complete ambos campos")
        return

    insert(name, phone)
    contacts.append([len(contacts) + 1, name, phone, date])
    update_table()
    input_name.delete(0, tk.END)
    input_phone.delete(0, tk.END)

# Función para actualizar la tabla
def update_table():
    agenda.delete(*agenda.get_children())
    for contact in view():
        agenda.insert("", "end", values=(contact[0], contact[1], contact[2], datetime.now().strftime("%Y-%m-%d")))

# Función para eliminar el contacto seleccionado
def remove_selected():
    select = agenda.selection()
    if not select:
        messagebox.showwarning("Eliminar", "Seleccione un contacto para eliminar")
        return

    contact = agenda.item(select, "values")
    if contact:
        delete(contact[0])
        update_table()

# Función para actualizar un contacto seleccionado
def update_selected():
    selected = agenda.selection()
    if not selected:
        messagebox.showwarning("Actualizar", "Seleccione un contacto para actualizar")
        return

    name = input_name.get().strip()
    phone = input_phone.get().strip()

    if not name or not phone:
        messagebox.showwarning("Campos Vacíos", "Debe llenar ambos campos para actualizar")
        return

    contact = agenda.item(selected, "values")
    if contact:
        update(contact[0], name, phone)
        update_table()
        input_name.delete(0, tk.END)
        input_phone.delete(0, tk.END)

# Función para filtrar los contactos por búsqueda
def search():
    search_term = search_var.get().strip().lower()
    agenda.delete(*agenda.get_children())
    for contact in view():
        if search_term in contact[1].lower() or search_term in contact[2].lower():
            agenda.insert("", "end", values=(contact[0], contact[1], contact[2], datetime.now().strftime("%Y-%m-%d")))

# Botones
btn_add = tk.Button(win, text="AÑADIR", command=add, bg="#4caf50", fg="white")
btn_remove = tk.Button(win, text="ELIMINAR", command=remove_selected, bg="#f44336", fg="white")
btn_update = tk.Button(win, text="ACTUALIZAR", command=update_selected, bg="#2196f3", fg="white")
btn_search = tk.Button(win, text="BUSCAR", command=search, bg="#ff9800", fg="white")

# Organizar elementos
grid_params = {"padx": 5, "pady": 5}
label_name.grid(row=0, column=0, **grid_params)
input_name.grid(row=0, column=1, **grid_params)
label_phone.grid(row=0, column=2, **grid_params)
input_phone.grid(row=0, column=3, **grid_params)

btn_add.grid(row=1, column=0, **grid_params)
btn_remove.grid(row=1, column=1, **grid_params)
btn_update.grid(row=1, column=2, **grid_params)

search_label.grid(row=1, column=3, **grid_params)
search_entry.grid(row=1, column=4, **grid_params)
btn_search.grid(row=1, column=5, **grid_params)

agenda.grid(row=2, column=0, columnspan=6, pady=10)

# Vincular la tecla Enter con la función añadir
win.bind("<Return>", lambda event: add())

# Actualizar la tabla al iniciar
update_table()

#Hacer que la pantalla se abra e el centro de la pantalla
win.eval('tk::PlaceWindow . center')

# Ejecutar la aplicación
win.mainloop()
