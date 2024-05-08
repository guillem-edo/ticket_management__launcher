import tkinter as tk
from tkinter import ttk, messagebox

# Función para enviar datos según la pestaña activa
def enviar_datos(tipo):
    data = entradas[tipo].get().strip()
    incidencia_seleccionada = incidencias_seleccionadas[tipo].get()
    if not data:
        messagebox.showwarning("Advertencia", f"Por favor, introduce datos para {tipo}.")
        return

    if incidencia_seleccionada == "":
        messagebox.showwarning("Advertencia", f"Por favor, selecciona una incidencia para {tipo}.")
        return

    messagebox.showinfo("Información", f"{tipo} - {incidencia_seleccionada}: {data}")

# Configuración de la ventana principal
app = tk.Tk()
app.title("Gestión de Incidencias")
app.geometry("600x450")

# Estilo personalizado
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f5f5f5")
style.configure("TLabel", font=("Helvetica", 14), background="#f5f5f5")
style.configure("TEntry", font=("Helvetica", 12), padding=5)
style.configure("TButton", font=("Helvetica", 12), padding=8)
style.configure("TNotebook", background="#f5f5f5")
style.configure("TNotebook.Tab", font=("Helvetica", 12), padding=[10, 5])

# Crear pestañas para categorías de incidencias
notebook = ttk.Notebook(app)
notebook.pack(pady=20, expand=True)

# Diccionarios para almacenar las entradas y las incidencias seleccionadas
entradas = {}
incidencias_seleccionadas = {}

# Crear pestaña para WC47 NACP
incidencias_wc47_nacp = [
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

frame_wc47_nacp = ttk.Frame(notebook, padding=20)
notebook.add(frame_wc47_nacp, text="WC47 NACP")

label_wc47_nacp = ttk.Label(frame_wc47_nacp, text="Describe la incidencia para WC47 NACP:", style="TLabel")
label_wc47_nacp.pack(pady=(0, 10))

incidencia_combo = ttk.Combobox(frame_wc47_nacp, values=incidencias_wc47_nacp, state="readonly", style="TEntry")
incidencia_combo.pack(pady=(0, 10))
incidencia_combo.set("")  # Inicialmente vacío
incidencias_seleccionadas["WC47 NACP"] = incidencia_combo

entry_wc47_nacp = ttk.Entry(frame_wc47_nacp, width=40, style="TEntry")
entry_wc47_nacp.pack(pady=10)
entradas["WC47 NACP"] = entry_wc47_nacp

button_wc47_nacp = ttk.Button(frame_wc47_nacp, text="Enviar", command=lambda: enviar_datos("WC47 NACP"), style="TButton")
button_wc47_nacp.pack(pady=20)

app.mainloop()
