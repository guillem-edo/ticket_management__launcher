import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from collections import defaultdict
import pandas as pd
from datetime import datetime, timedelta

class TurnChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.incident_details = None
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def set_incident_details(self, incident_details):
        self.incident_details = incident_details
        self.update_chart()

    def update_chart(self):
        if not self.incident_details:
            return

        # Procesar los datos para contar incidencias por turnos (cada 6 horas)
        incident_data = []
        for block, incidents in self.incident_details.items():
            for incident, count in incidents.items():
                # Extraer la fecha y hora del formato de texto de la incidencia
                parts = incident.split()
                if len(parts) >= 3:
                    try:
                        incident_time = datetime.strptime(parts[-2], '%H:%M:%S')
                        for _ in range(count):
                            incident_data.append({
                                'block': block,
                                'incident': " ".join(parts[:-3]),  # Excluyendo la fecha y la hora
                                'timestamp': incident_time
                            })
                    except ValueError:
                        continue

        if not incident_data:
            return

        df = pd.DataFrame(incident_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df = df.resample('6H').size()

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        bars = ax.bar(df.index, df.values, color=plt.get_cmap("tab10").colors)

        ax.set_title("Incidencias por Turnos (cada 6 horas)")
        ax.set_xlabel("Turnos")
        ax.set_ylabel("Número de Incidencias")
        ax.grid(True)

        total_incidents = df.sum()
        for bar in bars:
            height = bar.get_height()
            percentage = (height / total_incidents) * 100 if total_incidents > 0 else 0
            ax.annotate(f'{height}\n({percentage:.1f}%)',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

        self.canvas.draw()