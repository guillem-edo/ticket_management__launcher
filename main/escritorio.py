import tkinter as tk
from tkinter import ttk, messagebox

# Función para confirmar la incidencia seleccionada según el bloque activo
def confirmar_datos(tipo):
    incidencia_seleccionada = incidencias_seleccionadas[tipo].get()
    if not incidencia_seleccionada:
        messagebox.showwarning("Advertencia", f"Por favor, selecciona una incidencia para {tipo}.")
        return

    messagebox.showinfo("Validación de la incidencia", f"{tipo} \nIncidencia confirmada:\n\n{incidencia_seleccionada}")

# Configuración de la ventana principal
app = tk.Tk()
app.title("Gestor de Incidencias")
app.geometry("650x550")

# Estilo personalizado
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#e0f7fa")
style.configure("TLabel", font=("Arial", 14, "bold"), background="#e0f7fa", foreground="#006064")
style.configure("TRadiobutton", font=("Arial", 12), background="#e0f7fa", foreground="#004d40")
style.configure("TButton", font=("Arial", 12, "bold"), padding=10, background="#004d40", foreground="#ffffff")
style.map("TButton", foreground=[("active", "#ffffff"), ("!disabled", "#ffffff")], background=[("active", "#004d40"), ("!disabled", "#00796b")])
style.configure("TNotebook", background="#004d40", borderwidth=1)
style.configure("TNotebook.Tab", font=("Arial", 12, "bold"), padding=[10, 5], background="#b2ebf2", foreground="#006064")
style.map("TNotebook.Tab", background=[("selected", "#80deea")], foreground=[("selected", "#006064")])

# Crear pestañas para categorías de incidencias
notebook = ttk.Notebook(app)
notebook.pack(pady=20, expand=True)

# Diccionario para almacenar las incidencias seleccionadas
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

# Función para crear cada pestaña con opciones y botón de confirmación
def crear_pestana(nombre):
    frame = ttk.Frame(notebook, padding=20, style="TFrame")
    notebook.add(frame, text=nombre)

    label = ttk.Label(frame, text=f"Selecciona una incidencia para {nombre}:", style="TLabel")
    label.pack(pady=(0, 10))

    # Variable para almacenar la incidencia seleccionada
    selected = tk.StringVar()
    incidencias_seleccionadas[nombre] = selected

    # Crear radiobuttons para cada incidencia
    for incidencia in incidencias_comunes:
        radio = ttk.Radiobutton(frame, text=incidencia, value=incidencia, variable=selected, style="TRadiobutton")
        radio.pack(anchor='w', pady=(2, 2))

    button = ttk.Button(frame, text="Confirmar", command=lambda: confirmar_datos(nombre), style="TButton")
    button.pack(pady=20)

# Crear pestañas para cada bloque con las mismas incidencias
categorias = ["WC47 NACP", "WC48 Power 5F", "WC49 Power 5H", "WC50 Filter", "SPL"]
for categoria in categorias:
    crear_pestana(categoria)

app.mainloop()
