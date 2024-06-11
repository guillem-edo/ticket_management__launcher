from dependencies import *

<<<<<<< HEAD:beta_version/app/services/mtbf_dialog.py
class MTBFDisplay(QObject):

    def __init__(self, parent = None):
        self.parent = parent
        super().__init__()

    def show_mtbf_info(self, parent = None):
        dialog = QDialog(parent)
        dialog.setWindowTitle("Información sobre MTBF")
        dialog.setFixedSize(400, 200)
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(
            "MTBF (Mean Time Between Failures) es una métrica que indica el tiempo promedio entre fallas en un sistema. "
            "Se calcula tomando el tiempo total de operación dividido por el número de fallas ocurridas durante ese tiempo. "
            "En esta aplicación, el MTBF se muestra en minutos y se actualiza cada vez que se registra una incidencia. "
            "El valor se reinicia cada 24 horas."
        )
        layout.addWidget(text_edit)
        close_button = QPushButton("Cerrar")
        close_button.setStyleSheet(self.parent.get_button_style())
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        dialog.setLayout(layout)
        dialog.exec_()
=======
class MTBFDisplay:
    def __init__(self):
        self.mtbf_data = {}
        self.mtbf_labels = {}
>>>>>>> 1faa5ff97e308c736376616e21df72d5a2804e60:beta_version/app/mtbf_dialog.py

    def update_mtbf(self, block_name, timestamp):
        if block_name not in self.mtbf_data:
            self.mtbf_data[block_name] = {'last_time': None, 'total_time': 0, 'incident_count': 0}

        mtbf_info = self.mtbf_data[block_name]
        if mtbf_info["last_time"] is not None:
            time_diff = (timestamp - mtbf_info["last_time"]).total_seconds() / 60.0
            mtbf_info["total_time"] += time_diff
            mtbf_info["incident_count"] += 1
        else:
            mtbf_info["incident_count"] = 1
        
        mtbf_info["last_time"] = timestamp
        self.update_mtbf_display()

    def calculate_mtbf(self, block_name):
        if block_name in self.mtbf_data:
            mtbf_info = self.mtbf_data[block_name]
            if mtbf_info["incident_count"] > 0:
                mtbf = mtbf_info["total_time"] / mtbf_info["incident_count"]
                return f"{mtbf:.2f} minutos"
        return "N/A"

    def update_mtbf_display(self):
        for block, data in self.mtbf_data.items():
            if block in self.mtbf_labels:
                if data["incident_count"] > 0:
                    mtbf = data["total_time"] / data["incident_count"]
                    self.mtbf_labels[block].setText(f"MTBF {block}: {mtbf:.2f} minutos")
                else:
<<<<<<< HEAD:beta_version/app/services/mtbf_dialog.py
                    self.mtbf_labels[block].setText("MTBF {block}: N/A")
=======
                    self.mtbf_labels[block].setText(f"MTBF {block}: N/A")
>>>>>>> 1faa5ff97e308c736376616e21df72d5a2804e60:beta_version/app/mtbf_dialog.py

    def reset_mtbf_timer(self):
        self.mtbf_data = {block: {"total_time": 0, "incident_count": 0, "last_time": None} for block in self.mtbf_data.keys()}
        for block in self.mtbf_labels.keys():
            self.mtbf_labels[block].setText(f"MTBF {block}: N/A")
        self.schedule_daily_reset()

    def schedule_daily_reset(self):
        now = datetime.now()
        next_reset = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        delay = (next_reset - now).total_seconds() * 1000  # Convertir a milisegundos
        self.timer = QTimer()
        self.timer.singleShot(int(delay), self.reset_mtbf_timer)

    def load_mtbf_data(self):
        try:
            with open('mtbf_data.json', 'r') as f:
                mtbf_data_loaded = json.load(f)
                for block, data in mtbf_data_loaded.items():
                    if data['last_time'] is not None:
                        self.mtbf_data[block] = {
                            'total_time': data['total_time'],
                            'incident_count': data['incident_count'],
                            'last_time': datetime.strptime(data['last_time'], '%Y-%m-%d %H:%M:%S')
                        }
                    else:
                        self.mtbf_data[block] = {
                            'total_time': data['total_time'],
                            'incident_count': data['incident_count'],
                            'last_time': None
                        }
        except FileNotFoundError:
            self.mtbf_data = {}
        except Exception as e:
            print(f"Failed to load MTBF data: {e}")
            self.mtbf_data = {}

    def save_mtbf_data(self):
        mtbf_data_to_save = {}
        for block, data in self.mtbf_data.items():
            if data['last_time'] is not None:
                mtbf_data_to_save[block] = {
                    'total_time': data['total_time'],
                    'incident_count': data['incident_count'],
                    'last_time': data['last_time'].strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                mtbf_data_to_save[block] = {
                    'total_time': data['total_time'],
                    'incident_count': data['incident_count'],
                    'last_time': None
                }
        with open('mtbf_data.json', 'w') as f:
            json.dump(mtbf_data_to_save, f)
    
    
    def calculate_mtbf(self, block_name):
        if block_name in self.mtbf_data:
            mtbf_info = self.mtbf_data[block_name]
            if mtbf_info["incident_count"] > 0:
                mtbf = mtbf_info["total_time"] / mtbf_info["incident_count"]
                return f"{mtbf:.2f} minutos"
        return "N/A"
