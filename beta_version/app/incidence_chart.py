import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from collections import Counter, defaultdict
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class TurnChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.incident_details = {}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.chart_label = QLabel("Gráfico de Incidencias", self)
        self.chart_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.chart_label)
        layout.addWidget(self.canvas)

    def set_incident_details(self, incident_details):
        self.incident_details = incident_details
        self.update_charts()

    def update_charts(self, daily_incidents=None, shift_incidents=None):
        if daily_incidents:
            self.plot_daily_chart(daily_incidents, "Incidencias Diarias")
        if shift_incidents:
            self.plot_shift_chart(shift_incidents, "Incidencias por Turno")

    def plot_daily_chart(self, incidents, title):
        self.ax.clear()
        counts = Counter()
        for block, data in incidents.items():
            counts.update(data['incidences'])

        if not counts:
            return  # Si no hay incidencias, no se genera ningún gráfico

        labels, values = zip(*counts.items())
        total = sum(values)
        percentages = [f'{(value / total) * 100:.2f}%' for value in values]

        bars = self.ax.bar(labels, values, color='skyblue')

        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Incidencia', fontsize=12)
        self.ax.set_ylabel('Cantidad', fontsize=12)

        for bar, value, percentage in zip(bars, values, percentages):
            height = bar.get_height()
            self.ax.annotate(f'{value} ({percentage})',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        self.ax.tick_params(axis='x', rotation=45)
        self.figure.tight_layout()
        self.canvas.draw()

    def plot_shift_chart(self, incidents, title):
        self.ax.clear()
        counts = Counter()
        for block, data in incidents.items():
            counts.update(data['incidences'])

        if not counts:
            return  # Si no hay incidencias, no se genera ningún gráfico

        labels, values = zip(*counts.items())
        total = sum(values)
        percentages = [f'{(value / total) * 100:.2f}%' for value in values]

        bars = self.ax.bar(labels, values, color='lightcoral')

        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Incidencia', fontsize=12)
        self.ax.set_ylabel('Cantidad', fontsize=12)

        for bar, value, percentage in zip(bars, values, percentages):
            height = bar.get_height()
            self.ax.annotate(f'{value} ({percentage})',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        self.ax.tick_params(axis='x', rotation=45)
        self.figure.tight_layout()
        self.canvas.draw()

    def plot_general_chart(self, incidents, title):
        self.ax.clear()
        counts = defaultdict(Counter)
        for block, data in incidents.items():
            counts[block].update(data['incidences'])

        if not counts:
            return  # Si no hay incidencias, no se genera ningún gráfico

        colors = plt.cm.tab20.colors  # Usamos un colormap con suficientes colores

        all_labels = sorted({label for counter in counts.values() for label in counter})
        bottom = [0] * len(all_labels)

        for idx, (block, counter) in enumerate(counts.items()):
            values = [counter[label] for label in all_labels]
            bars = self.ax.barh(all_labels, values, left=bottom, color=colors[idx % len(colors)], label=block)
            bottom = [i + j for i, j in zip(bottom, values)]
            for bar, value in zip(bars, values):
                if value > 0:
                    width = bar.get_width()
                    self.ax.annotate(f'{value}',
                                    xy=(width, bar.get_y() + bar.get_height() / 2),
                                    xytext=(3, 0),  # 3 points horizontal offset
                                    textcoords="offset points",
                                    ha='left', va='center')

        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Cantidad', fontsize=12)
        self.ax.set_ylabel('Incidencia', fontsize=12)
        self.ax.legend(title="Bloques")

        self.ax.tick_params(axis='x', rotation=45)
        self.figure.tight_layout()
        self.canvas.draw()
