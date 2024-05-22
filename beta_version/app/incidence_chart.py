import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from datetime import datetime, timedelta

class IncidenceChart(QWidget):
    def __init__(self, incident_details, parent=None):
        super().__init__(parent)
        self.incident_details = incident_details

        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QWidget.Expanding, QWidget.Expanding)
        self.canvas.updateGeometry()

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.update_chart()

    def update_chart(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        now = datetime.now()
        times = [now - timedelta(hours=i) for i in range(24)][::-1]  # Últimas 24 horas

        for block, incidents in self.incident_details.items():
            counts = [0] * 24
            for incident, count in incidents.items():
                try:
                    incident_time = datetime.strptime(incident.split()[-2], "%H:%M:%S")
                    incident_hour = incident_time.hour
                    counts[23 - (now.hour - incident_hour)] += count
                except ValueError:
                    continue

            ax.plot([time.strftime("%H:%M") for time in times], counts, label=block)

        ax.set_title("Incidencias por Bloque en las Últimas 24 Horas")
        ax.set_xlabel("Hora")
        ax.set_ylabel("Número de Incidencias")
        ax.legend()
        self.canvas.draw()

    def set_incident_details(self, incident_details):
        self.incident_details = incident_details
        self.update_chart()