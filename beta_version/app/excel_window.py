from app.dependencies import *

class ExcelWindow(QMainWindow):
    def __init__(self, excel_file):
        super().__init__()
        self.excel_file = excel_file
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Visualización de Excel")
        self.resize(800, 600)
        self.center_window_app()

        main_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.table_widget = QTableWidget(self)
        self.table_widget.setStyleSheet("QTableWidget { font-size: 14px; }")
        main_layout.addWidget(self.table_widget)

        button_layout = QHBoxLayout()
        self.export_csv_button = QPushButton("Exportar a CSV", self)
        self.export_csv_button.clicked.connect(self.export_to_csv)
        button_layout.addWidget(self.export_csv_button)

        close_button = QPushButton("Cerrar", self)
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)

        main_layout.addLayout(button_layout)

        self.load_excel_file()
    
    def center_window_app(self):
        screen_geometry = QApplication.desktop().availableGeometry()
        window_width = int(screen_geometry.width() * 0.6)
        window_height = int(screen_geometry.height() * 0.6)
        self.resize(window_width, window_height)
        screen_center = screen_geometry.center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

    def load_excel_file(self):
        if self.excel_file and os.path.exists(self.excel_file):
            try:
                workbook = load_workbook(self.excel_file)
                sheet = workbook.active
                rows_to_display = list(sheet.iter_rows(min_row=2, values_only=True))

                self.table_widget.setRowCount(len(rows_to_display))
                self.table_widget.setColumnCount(sheet.max_column)

                headers = [cell.value for cell in sheet[1]]
                self.table_widget.setHorizontalHeaderLabels(headers)

                for row_idx, row in enumerate(rows_to_display):
                    for col_idx, cell_value in enumerate(row):
                        item = QTableWidgetItem(str(cell_value) if cell_value is not None else "")
                        self.table_widget.setItem(row_idx, col_idx, item)

                self.style_excel_table()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar el archivo Excel: {e}")

    def style_excel_table(self):
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #f9f9f9;
                alternate-background-color: #e0e0e0;
                border: 1px solid #ccc;
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 5px;
                border: 1px solid #ddd;
            }
        """)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.resizeColumnsToContents()

    def export_to_csv(self):
        if self.excel_file and os.path.exists(self.excel_file):
            file_dialog = QFileDialog()
            csv_path, _ = file_dialog.getSaveFileName(self, "Guardar archivo CSV", "", "CSV Files (*.csv)")
            if csv_path:
                try:
                    workbook = load_workbook(self.excel_file)
                    sheet = workbook.active
                    with open(csv_path, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        for row in sheet.iter_rows(values_only=True):
                            writer.writerow(row)
                    QMessageBox.information(self, "Exportación Completa", "Los datos han sido exportados correctamente a CSV.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al exportar a CSV: {e}")