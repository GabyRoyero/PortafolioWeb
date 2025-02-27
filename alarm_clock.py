import sys
import pygame
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTimeEdit, QPushButton, QListWidget, QMessageBox
from PyQt5.QtCore import QTimer, QTime

class AlarmClock(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.alarms = []
        self.load_alarms()
        pygame.mixer.init()

    def initUI(self):
        self.setWindowTitle("Despertador")
        self.setGeometry(100, 100, 300, 300)
        
        # Modo oscuro
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        
        self.label = QLabel("Selecciona una hora para la alarma:")
        layout.addWidget(self.label)
        
        self.time_edit = QTimeEdit()
        layout.addWidget(self.time_edit)
        
        self.set_alarm_button = QPushButton("Guardar Alarma")
        self.set_alarm_button.clicked.connect(self.add_alarm)
        layout.addWidget(self.set_alarm_button)
        
        self.alarm_list = QListWidget()
        layout.addWidget(self.alarm_list)
        
        self.delete_button = QPushButton("Eliminar Alarma")
        self.delete_button.clicked.connect(self.delete_alarm)
        layout.addWidget(self.delete_button)
        
        self.setLayout(layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_alarm)
        self.timer.start(1000)  # Verificar cada segundo

    def add_alarm(self):
        time = self.time_edit.time().toString("hh:mm AP")
        if time not in self.alarms:
            self.alarms.append(time)
            self.alarm_list.addItem(time)
            self.save_alarms()
        else:
            QMessageBox.warning(self, "Error", "Esta alarma ya existe.")

    def delete_alarm(self):
        selected_item = self.alarm_list.currentItem()
        if selected_item:
            self.alarms.remove(selected_item.text())
            self.alarm_list.takeItem(self.alarm_list.row(selected_item))
            self.save_alarms()
        else:
            QMessageBox.warning(self, "Error", "Selecciona una alarma para eliminar.")

    def save_alarms(self):
        with open("alarms.json", "w") as f:
            json.dump(self.alarms, f)

    def load_alarms(self):
        try:
            with open("alarms.json", "r") as f:
                self.alarms = json.load(f)
                self.alarm_list.addItems(self.alarms)
        except FileNotFoundError:
            self.alarms = []

    def check_alarm(self):
        current_time = QTime.currentTime().toString("hh:mm AP")
        if current_time in self.alarms:
            self.play_sound()
            QMessageBox.information(self, "Alarma", f"Es hora: {current_time}")
            self.alarms.remove(current_time)  # Eliminar alarma tras activarse
            self.save_alarms()
            self.alarm_list.clear()
            self.alarm_list.addItems(self.alarms)

    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load(r"C:\Users\gabyr\OneDrive\Desktop\Programación\Proyectos_cv\njz.mp3")
        pygame.mixer.music.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AlarmClock()
    window.show()
    sys.exit(app.exec_())
