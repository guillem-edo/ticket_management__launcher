import tkinter as tk
from tkinter import ttk, messagebox

# Función para confirmar la incidencia seleccionada según el bloque activo
def confirmar_datos(tipo):
    incidencia_seleccionada = incidencias_seleccionadas[tipo].get()
    if not incidencia_seleccionada:
        messagebox.showwarning("Advertencia", f"Por favor, selecciona una incidencia para {tipo}.")
        return

    messagebox.showinfo("Validación", f"{tipo} \nIncidencia confirmada: \n\n{incidencia_seleccionada}")

# Configuración de la ventana principal
app = tk.Tk()
app.title("Ticket Management")
app.geometry("1200x800")  # Tamaño grande pero no pantalla completa
app.iconbitmap('main\icon.ico')

# Estilo personalizado
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#2C3E50")
style.configure("TLabel", font=("Arial", 16, "bold"), background="#2C3E50", foreground="#ECF0F1")
style.configure("TRadiobutton", font=("Arial", 14), background="#34495E", foreground="#ECF0F1", indicatoron=0, width=30, padding=10)
style.configure("TButton", font=("Arial", 14, "bold"), padding=10, background="#3498DB", foreground="#ECF0F1")
style.map("TButton", foreground=[("active", "#ECF0F1"), ("!disabled", "#ECF0F1")], background=[("active", "#2980B9"), ("!disabled", "#3498DB")])
style.configure("TNotebook", background="#34495E", borderwidth=0)
style.configure("TNotebook.Tab", font=("Arial", 14, "bold"), padding=[20, 10], background="#95A5A6", foreground="#2C3E50")
style.map("TNotebook.Tab", background=[("selected", "#7F8C8D")], foreground=[("selected", "#2C3E50")])

# Crear pestañas para categorías de incidencias
notebook = ttk.Notebook(app)
notebook.pack(pady=20, padx=20, expand=True, fill='both')

# Diccionario para almacenar las incidencias seleccionadas
incidencias_seleccionadas = {}

# Lista de incidencias para "WC47 NACP"
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

# Lista de incidencias para "WC48 Power 5F"
incidencias_wc48_power_5f = [
    "Etiquetadora",
    "AOI (fallo etiqueta)",
    "AOI (malla)",
    "Cámara no detecta Pcb",
    "Cámara no detecta skeleton",
    "Cámara no detecta foams",
    "Cámara no detecta busbar",
    "Cámara no detecta foam derecho",
    "No detecta presencia power CP",
    "Tornillo atascado en tolva",
    "Cámara no detecta Power CP",
    "Cámara no detecta Top cover",
    "Detección de sealling mal puesto",
    "Robot no coge busbar",
    "Fallo etiqueta",
    "Power atascado en prensa, cuesta sacar",
    "No coloca bien el sealling"
]

# Lista de incidencias para "WC49 Power 5H"
incidencias_wc49_power_5h = [
    "La cámara no detecta Busbar",
    "La cámara no detecta Top Cover",
    "Screw K30 no lo detecta puesto",
    "Atasco tuerca",
    "Tornillo atascado",
    "Etiquetadora",
    "Detección de sealling mal puesto",
    "No coloca bien el sealling",
    "Power atascado en prensa, cuesta sacar",
    "No lee QR"
]

# Lista de incidencias para "WC50 Filter"
incidencias_wc50_filter = [
    "Fallo cámara ferrite",
    "NOK Soldadura Plástico",
    "NOK Soldadura metal",
    "Traza",
    "NOK Soldad. Plástico+Metal",
    "Robot no coloca bien filter en palet",
    "No coloca bien la pcb",
    "QR desplazado",
    "Core enganchado",
    "Robot no coge PCB",
    "Fallo atornillador",
    "Pieza enganchada en HV Test",
    "Cover atascado",
    "Robot no coloca bien ferrita",
    "No coloca bien el core",
    "Fallo Funcional",
    "Fallo visión core",
    "Fallo cámara cover",
    "Repeat funcional",
    "Fallo cámara QR",
    "No coloca bien foam"
]

# Lista de incidencias para "SPL"
incidencias_spl = [
    "Sensor de PCB detecta que hay placa cuando no la hay",
    "No detecta marcas Power",
    "Colisión placas",
    "Fallo dispensación glue",
    "Marco atascado en parte inferior",
    "Soldadura defectuosa",
    "Error en sensor de salida"
]
# Función para crear cada pestaña con incidencias específicas
def crear_pestana(nombre, incidencias):
    frame = ttk.Frame(notebook, padding=20, style="TFrame")
    notebook.add(frame, text=nombre)

    # Variable para almacenar la incidencia seleccionada
    selected = tk.StringVar()
    incidencias_seleccionadas[nombre] = selected

    # Crear botones para cada incidencia
    for incidencia in incidencias:
        button = ttk.Radiobutton(frame, text=incidencia, value=incidencia, variable=selected, style="TRadiobutton")
        button.pack(fill='x', padx=50, pady=5)

    # Botón confirmar para cada pestaña
    confirm_button = ttk.Button(frame, text="Confirmar", command=lambda: confirmar_datos(nombre), style="TButton")
    confirm_button.pack(pady=20, padx=100, side='bottom', fill='x')

# Crear pestañas para cada bloque
crear_pestana("WC47 NACP", incidencias_wc47_nacp)
crear_pestana("WC48 Power 5F", incidencias_wc48_power_5f)
crear_pestana("WC49 Power 5H", incidencias_wc49_power_5h)
crear_pestana("WC50 Filter", incidencias_wc50_filter)
crear_pestana("SPL", incidencias_spl)

app.mainloop()
