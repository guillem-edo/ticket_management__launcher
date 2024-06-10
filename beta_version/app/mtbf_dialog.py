from dependencies import *

class MTBFDisplay():

    def __init__(self):
        self.mtbf_data = {}
        self.mtbf_labels = {}

    def update_mtbf(self, block_name, timestamp):
        if block_name in self.mtbf_data:
            mtbf_info = self.mtbf_data[block_name]
            if mtbf_info["last_time"] is not None:
                time_diff = (timestamp - mtbf_info["last_time"]).total_seconds() / 60.0
                mtbf_info["total_time"] += time_diff
                mtbf_info["incident_count"] += 1
            mtbf_info["last_time"] = timestamp
            self.update_mtbf_display()

    def update_mtbf_display(self):
        if self.mtbf_data is None:
            self.mtbf_data = {}  # Asegurarse de que self.mtbf_data es un diccionario si era None.
            print("MTBF data was None, initialized to empty dictionary.")

        for block, data in self.mtbf_data.items():
            if block in self.mtbf_labels:
                if data["incident_count"] > 0:
                    mtbf = data["total_time"] / data["incident_count"]
                    self.mtbf_labels[block].setText(f"MTBF {block}: {mtbf:.2f} minutos")
                else:
                    self.mtbf_labels[block].setText("MTBF {block}: N/A")


    def reset_mtbf_timer(self):
        """Reinicia el temporizador para el cálculo del MTBF."""
        self.mtbf_data = {block: {"total_time": 0, "incident_count": 0} for block in self.mtbf_data.keys()}
        for block in self.mtbf_labels.keys():
            self.mtbf_labels[block].setText(f"MTBF {block}: N/A")

        # Asegúrate de que el temporizador se reinicia cada 24 horas
        self.schedule_daily_reset()

    def schedule_daily_reset(self):
        now = datetime.now()
        next_reset = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        delay = (next_reset - now).total_seconds() * 1000  # Convertir a milisegundos
        self.timer = QTimer()
        self.timer.singleShot(int(delay), self.reset_mtbf_timer)

    def reset_mtbf_data(self):
        if self.mtbf_data is not None:
            for block in self.mtbf_data.keys():
                self.mtbf_data[block] = {'last_time': None, 'total_time': 0, 'incident_count': 0}
        else:
            print("MTBF data is not initialized.")

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
            print("MTBF data file not found. Initializing with empty data.")
            self.mtbf_data = {block: {'last_time': None, 'total_time': 0, 'incident_count': 0} for block in self.incidencias.keys()}
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