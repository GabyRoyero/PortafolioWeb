from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
import sys
import calendar

class CalendarioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Calendario")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Ingresa el año que deseas:")
        layout.addWidget(self.label)

        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        self.btn = QPushButton("Mostrar Calendario")
        self.btn.clicked.connect(self.mostrar_calendario)
        layout.addWidget(self.btn)

        self.Result = QTextEdit()
        self.Result.setReadOnly(True)
        layout.addWidget(self.Result)

        self.setLayout(layout)

    def mostrar_calendario(self):
        try:
            yy = int(self.text_input.text())
            if yy < 0 or yy >3000:
                self.Result.setText("Ingrese un año entre 0 y 3000:")
            else:
             self.Result.clear()

             columnas = 3
             fila = 0
             columna = 0

             for mm in range(1, 13):
                 mes_calendario = calendar.month(yy, mm)
                 self.Result.append(f"{mes_calendario}\n")

                 columna += 1
                 if columna == columnas:
                     columna = 0
                     fila += 1
        except:
            self.Result.setText("Por favor, igrese solo números.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = CalendarioApp()
    ventana.show()
    sys.exit(app.exec_())