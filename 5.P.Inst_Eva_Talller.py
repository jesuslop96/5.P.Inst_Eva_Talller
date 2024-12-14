import mysql.connector
import tkinter as tk
from tkinter import messagebox

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def conectar_db(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Conexión establecida a la base de datos")
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            messagebox.showerror("Error de conexión", f"Error al conectar a la base de datos: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")

    def insertar_miembro(self, nombre, email, telefono, fecha_registro):
        if not nombre or not email or not fecha_registro:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            self.cursor.callproc('insertar_miembro', (nombre, email, telefono, fecha_registro))
            self.connection.commit()
            messagebox.showinfo("Éxito", "Miembro insertado correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al insertar miembro: {err}")

    def actualizar_miembro(self, miembro_id, nombre, email, telefono, fecha_registro):
        if not miembro_id or not nombre or not email or not fecha_registro:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            self.cursor.callproc('actualizar_miembro', (int(miembro_id), nombre, email, telefono, fecha_registro))
            self.connection.commit()
            messagebox.showinfo("Éxito", "Miembro actualizado correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al actualizar miembro: {err}")

    def eliminar_miembro(self, miembro_id):
        if not miembro_id:
            messagebox.showerror("Error", "El ID del miembro es obligatorio.")
            return

        try:
            self.cursor.callproc('eliminar_miembro', (int(miembro_id),))
            self.connection.commit()
            messagebox.showinfo("Éxito", "Miembro eliminado correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar miembro: {err}")

# Crear la ventana principal de Tkinter
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Gimnasio")

        # Conectar a la base de datos
        self.db_connector = DatabaseConnector("localhost", "root", "", "gym")
        self.db_connector.conectar_db()

        # Configurar la interfaz gráfica
        self.frame = tk.Frame(self)
        self.frame.pack(padx=10, pady=10)

        # Campos de entrada para miembro
        self.entry_id_miembro = tk.Entry(self.frame)
        self.entry_id_miembro.grid(row=0, column=1, pady=5)
        tk.Label(self.frame, text="ID Miembro").grid(row=0, column=0, pady=5)

        self.entry_nombre = tk.Entry(self.frame)
        self.entry_nombre.grid(row=1, column=1, pady=5)
        tk.Label(self.frame, text="Nombre").grid(row=1, column=0, pady=5)

        self.entry_email = tk.Entry(self.frame)
        self.entry_email.grid(row=2, column=1, pady=5)
        tk.Label(self.frame, text="Email").grid(row=2, column=0, pady=5)

        self.entry_telefono = tk.Entry(self.frame)
        self.entry_telefono.grid(row=3, column=1, pady=5)
        tk.Label(self.frame, text="Teléfono").grid(row=3, column=0, pady=5)

        self.entry_fecha_registro = tk.Entry(self.frame)
        self.entry_fecha_registro.grid(row=4, column=1, pady=5)
        tk.Label(self.frame, text="Fecha Registro (YYYY-MM-DD)").grid(row=4, column=0, pady=5)

        # Botones para las acciones
        tk.Button(self.frame, text="Insertar Miembro", command=self.insertar_miembro).grid(row=5, column=0, pady=10)
        tk.Button(self.frame, text="Actualizar Miembro", command=self.actualizar_miembro).grid(row=5, column=1, pady=10)
        tk.Button(self.frame, text="Eliminar Miembro", command=self.eliminar_miembro).grid(row=6, column=0, pady=10)

    def insertar_miembro(self):
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        telefono = self.entry_telefono.get()
        fecha_registro = self.entry_fecha_registro.get()
        self.db_connector.insertar_miembro(nombre, email, telefono, fecha_registro)

    def actualizar_miembro(self):
        miembro_id = self.entry_id_miembro.get()
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        telefono = self.entry_telefono.get()
        fecha_registro = self.entry_fecha_registro.get()
        self.db_connector.actualizar_miembro(miembro_id, nombre, email, telefono, fecha_registro)

    def eliminar_miembro(self):
        miembro_id = self.entry_id_miembro.get()
        self.db_connector.eliminar_miembro(miembro_id)

    def on_closing(self):
        self.db_connector.disconnect()
        self.destroy()


if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
