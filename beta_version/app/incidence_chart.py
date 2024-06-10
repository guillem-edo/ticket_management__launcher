from dependencies import *

class TurnChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.incident_details = {}
        self.figure = None  # Inicializa sin figura
        self.canvas = None  # Inicializa sin canvas
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.chart_label = QLabel("", self)
        self.chart_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.chart_label)

    def set_incident_details(self, incident_details):
        self.incident_details = incident_details
        self.update_charts()

    def update_charts(self, daily_incidents=None, shift_incidents=None):
        if daily_incidents:
            self.plot_daily_chart(daily_incidents, "Incidencias Diarias")
        if shift_incidents:
            self.plot_shift_chart(shift_incidents, "Incidencias por Turno")

    def plot_daily_chart(self, incidents, title):
        self._plot_chart(incidents, title, 'skyblue')

    def plot_shift_chart(self, incidents, title):
        self._plot_chart(incidents, title, 'lightcoral')

    def plot_general_chart(self, incidents, title):
        counts = defaultdict(Counter)
        for block, data in incidents.items():
            counts[block].update(data['incidences'])

        if not counts:
            return  # Si no hay incidencias, no se genera ningún gráfico

        if self.figure:
            plt.close(self.figure)  # Cerrar cualquier figura antigua

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)  # Crear el canvas de la figura
        layout = self.layout()
        layout.addWidget(self.canvas)  # Añadir el canvas al layout

        ax = self.figure.add_subplot(111)
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
        ax.legend(title="Linias", bbox_to_anchor=(1.05, 1), loc='upper left')  # Ajustar la leyenda para que no solape las barras

        plt.xticks(rotation=45, ha='right')
        try:
            self.figure.tight_layout()
        except ValueError:
            pass  # Si tight_layout falla, solo continuamos sin él

        self.canvas.draw()  # Asegurarse de actualizar el canvas

    def _plot_chart(self, incidents, title, color):
        counts = Counter()
        for block, data in incidents.items():
            counts.update(data['incidences'])

        if not counts:
            return  # Si no hay incidencias, no se genera ningún gráfico

        if self.figure:
            plt.close(self.figure)  # Cerrar cualquier figura antigua

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)  # Crear el canvas de la figura
        layout = self.layout()
        layout.addWidget(self.canvas)  # Añadir el canvas al layout

        labels, values = zip(*counts.items())
        total = sum(values)
        percentages = [f'{(value / total) * 100:.2f}%' for value in values]

        self.figure.clf()
        ax = self.figure.add_subplot(111)
        bars = ax.bar(labels, values, color=color)

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
        try:
            self.figure.tight_layout()
        except ValueError:
            pass  # Si tight_layout falla, solo continuamos sin él

        self.canvas.draw()  # Asegurarse de actualizar el canvas