from .dependencies import *

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

    def plot_daily_chart(self, incidents, title):
        self._plot_chart(incidents, title, horizontal=False)

    def plot_shift_chart(self, incidents, title):
        self._plot_chart(incidents, title, horizontal=False)

    def plot_general_chart(self, incidents, title):
        counts = defaultdict(Counter)
        for block, data in incidents.items():
            counts[block].update(data['incidences'])

        if not counts:
            return  # Si no hay incidencias, no se genera ningún gráfico

        if self.figure:
            plt.close(self.figure)  # Cerrar cualquier figura antigua

        self.figure = plt.figure(figsize=(8, 6))  # Ajustar el tamaño de la figura
        self.canvas = FigureCanvas(self.figure)  # Crear el canvas de la figura
        layout = self.layout()
        layout.addWidget(self.canvas)  # Añadir el canvas al layout

        ax = self.figure.add_subplot(111)
        colors = ["#bc6c25", "#219EBC", "#023047", "#FFB703", "#FB8500"]  # Usar la paleta de colores proporcionada

        all_labels = sorted({label for counter in counts.values() for label in counter})
        bottom = [0] * len(all_labels)

        # Mapa de colores por bloque
        block_colors = {block: colors[idx % len(colors)] for idx, block in enumerate(counts.keys())}

        for block, counter in counts.items():
            values = [counter[label] for label in all_labels]
            bars = ax.barh(all_labels, values, left=bottom, color=block_colors[block], label=block)
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
        ax.legend(title="Bloques", bbox_to_anchor=(1.05, 1), loc='upper left')  # Ajustar la leyenda para que no solape las barras

        ax.set_yticklabels([label if len(label) < 30 else label[:27] + '...' for label in all_labels], fontsize=10)  # Ajustar etiquetas largas

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout(pad=2.0)  # Ajustar el espaciado para acomodar la leyenda

        self.canvas.draw()  # Asegurarse de actualizar el canvas

    def _plot_chart(self, incidents, title, horizontal=True):
        counts = Counter()
        for block, data in incidents.items():
            counts.update(data['incidences'])

        if not counts:
            return  # Si no hay incidencias, no se genera ningún gráfico

        if self.figure:
            plt.close(self.figure)  # Cerrar cualquier figura antigua

        self.figure = plt.figure(figsize=(8, 6))  # Ajustar el tamaño de la figura
        self.canvas = FigureCanvas(self.figure)  # Crear el canvas de la figura
        layout = self.layout()
        layout.addWidget(self.canvas)  # Añadir el canvas al layout

        labels, values = zip(*counts.items())
        total = sum(values)
        percentages = [f'{(value / total) * 100:.2f}%' for value in values]

        self.figure.clf()
        ax = self.figure.add_subplot(111)

        if horizontal:
            bars = ax.barh(labels, values, color='skyblue')
        else:
            bars = ax.bar(labels, values, color='skyblue')

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Cantidad', fontsize=12)
        ax.set_ylabel('Incidencia', fontsize=12)

        for bar, value, percentage in zip(bars, values, percentages):
            if horizontal:
                width = bar.get_width()
                ax.annotate(f'{value} ({percentage})',
                            xy=(width, bar.get_y() + bar.get_height() / 2),
                            xytext=(3, 0),  # 3 points horizontal offset
                            textcoords="offset points",
                            ha='left', va='center')
            else:
                height = bar.get_height()
                ax.annotate(f'{value} ({percentage})',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout(pad=2.0)  # Ajustar el espaciado para acomodar la leyenda

        self.canvas.draw()  # Asegurarse de actualizar el canvas