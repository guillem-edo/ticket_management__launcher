import requests

def enviar_datos():
    data = entry.get()
    response = requests.post('http://localhost:5000/submit', json={'data': data})
    if response.status_code == 200:
        messagebox.showinfo("Éxito", "Datos enviados correctamente")
    else:
        messagebox.showerror("Error", "Error al enviar datos")
