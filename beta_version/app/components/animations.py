# animations.py
from PyQt5.QtCore import QPropertyAnimation

def fade_in(widget, duration=1000):
    animation = QPropertyAnimation(widget, b"windowOpacity")
    animation.setDuration(duration)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.start()
