import tkinter as tk
from tkinter import messagebox

def enviar_datos():
    data = entry.get()  # Obtiene los datos del campo de entrada
    # Aquí puedes añadir el código para enviar los datos a la API
    messagebox.showinfo("Información", f"Dato enviado: {data}")

app = tk.Tk()
app.title("Aplicación de Datos")

label = tk.Label(app, text="Introduce tus datos:")
label.pack(padx=20, pady=10)

entry = tk.Entry(app)
entry.pack(padx=20, pady=10)

button = tk.Button(app, text="Enviar", command=enviar_datos)
button.pack(padx=20, pady=20)

app.mainloop()