import sqlite3

def connect():
    conn = sqlite3.connect("agenda.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            telefono TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert(nombre, telefono):
    conn = sqlite3.connect("agenda.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contactos (nombre, telefono) VALUES (?, ?)", (nombre, telefono))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("agenda.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contactos")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect("agenda.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contactos WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(id, nombre, telefono):
    conn = sqlite3.connect("agenda.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE contactos SET nombre=?, telefono=? WHERE id=?", (nombre, telefono, id))
    conn.commit()
    conn.close()

connect()  # Crea la tabla si no existe
