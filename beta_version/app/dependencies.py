import os
import json
import csv
<<<<<<< HEAD
=======
import seaborn as sns
>>>>>>> 1faa5ff97e308c736376616e21df72d5a2804e60

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['figure.max_open_warning'] = 50

<<<<<<< HEAD
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
=======
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QComboBox, QHeaderView
>>>>>>> 1faa5ff97e308c736376616e21df72d5a2804e60
from functools import partial

from datetime import datetime, timedelta, time
from collections import Counter, defaultdict
<<<<<<< HEAD
from openpyxl import load_workbook, Workbook
=======
from openpyxl import Workbook, load_workbook
>>>>>>> 1faa5ff97e308c736376616e21df72d5a2804e60

from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox,
    QTabWidget, QLabel, QListWidget, QStatusBar, QSplitter, QAbstractItemView, QListWidgetItem, QInputDialog, QApplication, QDialog, QTextEdit
)
<<<<<<< HEAD
from PyQt5.QtCore import QTimer, Qt, QRect, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QFont, QIcon
from functools import partial
=======
from PyQt5.QtCore import QTimer, Qt, QRect # pyqtSlot
from PyQt5.QtGui import QFont, QIcon
from functools import partial
>>>>>>> 1faa5ff97e308c736376616e21df72d5a2804e60
