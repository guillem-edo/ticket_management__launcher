import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from collections import Counter, defaultdict

class TurnChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.incident_details = {}
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())
        self.chart_label = QLabel("Gráfico de Incidencias", self)
        self.chart_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout().addWidget(self.chart_label)

    def set_incident_details(self, incident_details):
        self.incident_details = incident_details
        self.update_charts()

    def update_charts(self, daily_incidents=None, shift_incidents=None):
        if daily_incidents:
            self.plot_daily_chart(daily_incidents, "Incidencias Diarias")
        if shift_incidents:
            self.plot_shift_chart(shift_incidents, "Incidencias por Turno")

    def plot_daily_chart(self, incidents, title):
        counts = Counter()
        for block, data in incidents.items():
            counts.update(data['incidences'])

        if not counts:
            return  # Si no hay incidencias, no se genera ningún gráfico

        labels, values = zip(*counts.items())
        total = sum(values)
        percentages = [f'{(value / total) * 100:.2f}%' for value in values]

        fig, ax = plt.subplots()
        bars = ax.bar(labels, values, color='skyblue')

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Incidencia', fontsize=12)
        ax.set_ylabel('Cantidad', fontsize=12)

        for bar, value, percentage in zip(bars, values, percentages):
            height = bar.get_height()
            ax.annotate(f'{value} ({percentage})',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def plot_shift_chart(self, incidents, title):
        counts = Counter()
        for block, data in incidents.items():
            counts.update(data['incidences'])

        if not counts:
            return  # Si no hay incidencias, no se genera ningún gráfico

        labels, values = zip(*counts.items())
        total = sum(values)
        percentages = [f'{(value / total) * 100:.2f}%' for value in values]

        fig, ax = plt.subplots()
        bars = ax.bar(labels, values, color='lightcoral')

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Incidencia', fontsize=12)
        ax.set_ylabel('Cantidad', fontsize=12)

        for bar, value, percentage in zip(bars, values, percentages):
            height = bar.get_height()
            ax.annotate(f'{value} ({percentage})',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def plot_general_chart(self, incidents, title):
        counts = defaultdict(Counter)
        for block, data in incidents.items():
            counts[block].update(data['incidences'])

        if not counts:
            return  # Si no hay incidencias, no se genera ningún gráfico

        fig, ax = plt.subplots()
        colors = plt.cm.tab20.colors  # Usamos un colormap con suficientes colores

        all_labels = sorted({label for counter in counts.values() for label in counter})
        bottom = [0] * len(all_labels)

        for idx, (block, counter) in enumerate(counts.items()):
            values = [counter[label] for label in all_labels]
            bars = ax.barh(all_labels, values, left=bottom, color=colors[idx % len(colors)], label=block)
            bottom = [i + j for i, j in zip(bottom, values)]
            for bar, value in zip(bars, values):
                if value > 0:
                    width = bar.get_width()
                    ax.annotate(f'{value}',
                                xy=(width, bar.get_y() + bar.get_height() / 2),
                                xytext=(3, 0),  # 3 points horizontal offset
                                textcoords="offset points",
                                ha='left', va='center')

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Cantidad', fontsize=12)
        ax.set_ylabel('Incidencia', fontsize=12)
        ax.legend(title="Bloques")

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()