import tkinter as tk
from tkinter import ttk, messagebox

# Función para enviar datos según la pestaña activa
def enviar_datos(tipo):
    data = entradas[tipo].get().strip()
    incidencia_seleccionada = incidencias_seleccionadas[tipo].get()
    if not data:
        messagebox.showwarning("Advertencia", f"Por favor, introduce datos para {tipo}.")
        return

    if not incidencia_seleccionada:
        messagebox.showwarning("Advertencia", f"Por favor, selecciona una incidencia para {tipo}.")
        return

    messagebox.showinfo("Información", f"{tipo} - {incidencia_seleccionada}: {data}")

# Configuración de la ventana principal
app = tk.Tk()
app.title("Gestión de Incidencias")
app.geometry("600x500")

# Estilo personalizado
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f5f5f5")
style.configure("TLabel", font=("Helvetica", 14), background="#f5f5f5")
style.configure("TEntry", font=("Helvetica", 12), padding=5)
style.configure("TButton", font=("Helvetica", 12), padding=8)
style.configure("TRadiobutton", font=("Helvetica", 12), background="#f5f5f5")
style.configure("TNotebook", background="#f5f5f5")
style.configure("TNotebook.Tab", font=("Helvetica", 12), padding=[10, 5])

# Crear pestañas para categorías de incidencias
notebook = ttk.Notebook(app)
notebook.pack(pady=20, expand=True)

# Diccionarios para almacenar las entradas y las incidencias seleccionadas
entradas = {}
incidencias_seleccionadas = {}

# Lista de incidencias común para todas las categorías
incidencias_comunes = [
    "Etiquetadora",
    "Fallo en elevador",
    "No atornilla tapa",
    "Fallo tolva",
    "Fallo en paletizador",
    "No coge placa",
    "Palet atascado en la curva",
    "Ascensor no sube",
    "No pone tornillo",
    "Fallo tornillo",
    "AOI no detecta pieza",
    "No atornilla clips",
    "Fallo fijador tapa",
    "Secuencia atornillador",
    "Fallo atornillador",
    "Fallo cámara visión"
]

# Función para crear cada pestaña con entrada, opciones y botón de envío
def crear_pestana(nombre):
    frame = ttk.Frame(notebook, padding=20)
    notebook.add(frame, text=nombre)

    label = ttk.Label(frame, text=f"Describe la incidencia para {nombre}:", style="TLabel")
    label.pack(pady=(0, 10))

    # Variable para almacenar la incidencia seleccionada
    selected = tk.StringVar()
    incidencias_seleccionadas[nombre] = selected

    # Crear radiobuttons para cada incidencia
    for incidencia in incidencias_comunes:
        radio = ttk.Radiobutton(frame, text=incidencia, value=incidencia, variable=selected, style="TRadiobutton")
        radio.pack(anchor='w', pady=(2, 2))

    entry = ttk.Entry(frame, width=40, style="TEntry")
    entry.pack(pady=10)
    entradas[nombre] = entry

    button = ttk.Button(frame, text="Enviar", command=lambda: enviar_datos(nombre), style="TButton")
    button.pack(pady=20)

# Crear pestañas para cada bloque con las mismas incidencias
categorias = ["WC47 NACP", "WC48 Power 5F", "WC49 Power 5H", "WC50 Filter", "SPL"]
for categoria in categorias:
    crear_pestana(categoria)

app.mainloop()
