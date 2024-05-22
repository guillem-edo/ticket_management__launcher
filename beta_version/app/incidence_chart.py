import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from datetime import datetime, timedelta

class IncidenceChart(QWidget):
    def __init__(self, incident_details, parent=None):
        super().__init__(parent)
        self.incident_details = incident_details

        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
                    date_str = incident.split()[-3]
                    incident_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if (now - incident_date).days <= 1:  # Solo considerar las incidencias de las últimas 24 horas
                        incident_time = datetime.strptime(incident.split()[-2], "%H:%M:%S")
                        incident_hour = incident_time.hour
                        counts[23 - (now.hour - incident_hour)] += count
                except (ValueError, IndexError):
                    continue

            ax.plot([time.strftime("%H:%M") for time in times], counts, label=block)

        ax.set_title("Incidencias por Bloque en las Últimas 24 Horas")
        ax.set_xlabel("Hora")
        ax.set_ylabel("Número de Incidencias")
        if ax.get_legend().get_texts():
            ax.legend()
        self.canvas.draw()

    def set_incident_details(self, incident_details):
        self.incident_details = incident_details
        self.update_chart()