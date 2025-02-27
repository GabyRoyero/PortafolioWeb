import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QGridLayout
from PyQt5.QtGui import QPalette, QColor

class ScientificCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculadora Científica')
        self.setGeometry(100, 100, 400, 500)
        
        # Modo oscuro
        self.setStyleSheet("background-color: #2E2E2E; color: white;")
        
        self.layout = QVBoxLayout()
        
        self.display = QLineEdit()
        self.display.setStyleSheet("background-color: #1C1C1C; color: white; font-size: 18px;")
        self.layout.addWidget(self.display)
        
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.history.setStyleSheet("background-color: #1C1C1C; color: lightgray;")
        self.layout.addWidget(self.history)
        
        self.grid = QGridLayout()
        
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('sin', 5, 1), ('cos', 5, 2), ('tan', 5, 3),
            ('log', 6, 0), ('exp', 6, 1), ('sqrt', 6, 2), ('^', 6, 3)
        ]
        
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setStyleSheet("background-color: #333; color: white; font-size: 16px;")
            button.clicked.connect(self.on_button_click)
            self.grid.addWidget(button, row, col)
        
        self.layout.addLayout(self.grid)
        self.setLayout(self.layout)
    
    def on_button_click(self):
        sender = self.sender().text()
        if sender == '=':
            try:
                expression = self.display.text()
                expression = expression.replace('^', '**')  # Para potencias
                result = str(eval(expression, {"math": math, "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log10, "exp": math.exp, "sqrt": math.sqrt}))
                self.history.append(f"{expression} = {result}")
                self.display.setText(result)
            except Exception as e:
                self.display.setText("Error")
        elif sender == 'C':
            self.display.clear()
        else:
            self.display.setText(self.display.text() + sender)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = ScientificCalculator()
    calc.show()
    sys.exit(app.exec_())
