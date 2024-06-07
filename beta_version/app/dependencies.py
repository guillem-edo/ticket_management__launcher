import os
import json
import csv

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['figure.max_open_warning'] = 50

from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from functools import partial

from datetime import datetime, timedelta, time
from collections import Counter, defaultdict
from openpyxl import Workbook, load_workbook

from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox,
    QTabWidget, QLabel, QListWidget, QStatusBar, QSplitter, QAbstractItemView, QListWidgetItem, QInputDialog, QApplication, QDialog, QTextEdit
)
from PyQt5.QtCore import QTimer, Qt, QRect # pyqtSlot
from PyQt5.QtGui import QFont, QIcon
from functools import partial