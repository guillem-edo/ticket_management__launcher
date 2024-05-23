import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
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
            print("No incident details to display in chart.")
            return

        print("Updating chart with incident details:", self.incident_details)

        # Procesar los datos para contar incidencias por turnos (cada 6 horas)
        incident_data = []
        for block, incidents in self.incident_details.items():
            for incident, count in incidents.items():
                incident_data.append({'block': block, 'incident': incident, 'count': count})

        if not incident_data:
            print("No incident data to plot.")
            return

        df = pd.DataFrame(incident_data)
        if df.empty:
            print("DataFrame is empty after parsing incident data.")
            return

        # Agrupar y contar las incidencias por bloques
        df_grouped = df.groupby('block')['count'].sum().reset_index()

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        bars = ax.bar(df_grouped['block'], df_grouped['count'], color=plt.get_cmap("tab10").colors)

        ax.set_title("Número de Incidencias por Bloque")
        ax.set_xlabel("Bloque")
        ax.set_ylabel("Número de Incidencias")
        ax.grid(True)

        total_incidents = df_grouped['count'].sum()
        for bar in bars:
            height = bar.get_height()
            percentage = (height / total_incidents) * 100 if total_incidents > 0 else 0
            ax.annotate(f'{height}\n({percentage:.1f}%)',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 puntos de offset vertical
                        textcoords="offset points",
                        ha='center', va='bottom')

        self.canvas.draw()