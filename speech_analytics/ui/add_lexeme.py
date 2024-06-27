import sys
from typing import Optional

from PyQt5.QtWidgets import QApplication, QDialog, QComboBox, QLineEdit, QPushButton, QSpinBox, QVBoxLayout, QLabel

from speech_analytics.bnf.parser import Parser
from speech_analytics.models.lexeme import Lexeme
from speech_analytics.models.token_type import TokenType


class AddLexeme(QDialog):
    def __init__(self):
        super().__init__()

        # Configuración básica del diálogo
        self.setWindowTitle('Agregar lexema')
        self.setGeometry(100, 100, 400, 200)

        # Widgets del diálogo
        self.label = QLabel('Ingrese palabra o frase:')
        self.lineEdit = QLineEdit()

        self.label2 = QLabel('Token:')
        self.comboBox = QComboBox()
        self.comboBox.addItems([token_type.title for token_type in TokenType])

        self.label3 = QLabel('Seleccione un número del 0 al 5:')
        self.spinBox = QSpinBox()
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(5)

        self.button = QPushButton('Aceptar')
        self.button.clicked.connect(self.accept)

        # Layout del diálogo
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.label2)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.label3)
        layout.addWidget(self.spinBox)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def get_data(self) -> Optional[Lexeme]:
        # Obtén los datos ingresados por el usuario
        text = self.lineEdit.text()

        if text is None or text == '':
            return None

        selected_title = self.comboBox.currentText()
        selected_token_type = next(token_type for token_type in TokenType if token_type.title == selected_title)
        weight = self.spinBox.value()
        parser = Parser(text)
        return Lexeme(parser.parse(), selected_token_type, weight)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AddLexeme()
    if dialog.exec_() == QDialog.Accepted:
        data = dialog.get_data()
        print("Texto:", data[0])
        print("Opción:", data[1])
        print("Número:", data[2])
    sys.exit(app.exec_())
