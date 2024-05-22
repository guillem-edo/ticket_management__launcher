import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from collections import defaultdict

class IncidenceChart(QWidget):
    def __init__(self, incident_details, parent=None):
        super().__init__(parent)
        self.incident_details = incident_details
        self.block_counts = defaultdict(int)  # Diccionario para contar incidencias por bloque

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

        # Contar incidencias por bloque
        self.block_counts = defaultdict(int)
        total_incidents = 0
        for block, incidents in self.incident_details.items():
            count = sum(incidents.values())
            self.block_counts[block] = count
            total_incidents += count

        blocks = list(self.block_counts.keys())
        counts = list(self.block_counts.values())

        bars = ax.bar(blocks, counts, color=plt.get_cmap("tab10").colors)

        ax.set_title("Incidencias Acumuladas")
        ax.set_xlabel("")
        ax.set_ylabel("Cantidad")
        ax.grid(True)

        # Añadir porcentajes encima de las barras
        for bar in bars:
            height = bar.get_height()
            percentage = (height / total_incidents) * 100 if total_incidents > 0 else 0
            ax.annotate(f'{height}\n({percentage:.1f}%)',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

        self.canvas.draw()

    def set_incident_details(self, incident_details):
        self.incident_details = incident_details
        self.update_chart()

    def add_incident(self, block_name):
        self.block_counts[block_name] += 1
        self.update_chart()