import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout,
    QWidget, QFileDialog, QMessageBox
)

from speech_analytics.bnf.parser import Parser
from speech_analytics.file_manager.file_manager import FileManager
from speech_analytics.minimal_tokenizer.minimal_tokenizer import MinimalTokenizer
from speech_analytics.models.role import Role
from speech_analytics.ui.add_lexeme import AddLexeme
from speech_analytics.ui.summary_window import SummaryWindow


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speech Analytics")

        self.client_text: str = ""
        self.agent_text: str = ""

        # Botón para abrir el archivo del cliente
        self.open_client_button = QPushButton("Abrir Archivo Cliente", self)
        self.open_client_button.clicked.connect(self.open_client_file)

        # Botón para abrir el archivo del agente
        self.open_agent_button = QPushButton("Abrir Archivo Agente", self)
        self.open_agent_button.clicked.connect(self.open_agent_file)

        # Botón para abrir el diálogo personalizado
        self.open_dialog_button = QPushButton("Agregar Lexema", self)
        self.open_dialog_button.clicked.connect(self.open_dialog)

        # Crear un área de texto para mostrar el contenido del archivo
        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.text_display.setLineWrapMode(QTextEdit.WidgetWidth)
        self.text_display.setFixedSize(800, 200)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.open_client_button)
        layout.addWidget(self.open_agent_button)
        layout.addWidget(self.open_dialog_button)
        layout.addWidget(self.text_display)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_client_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo Cliente", "",
                                                  "Text files (*.txt);;All files (*.*)")
        if not filepath:
            return

        with open(filepath, "r") as file:
            self.client_text = file.read()

        self.display_results(Role.CUSTOMER, self.client_text)

    def open_agent_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo Agente", "",
                                                  "Text files (*.txt);;All files (*.*)")
        if not filepath:
            return

        with open(filepath, "r") as file:
            self.agent_text = file.read()

        self.display_results(Role.AGENT, self.agent_text)

    def display_results(self, role: Role, text: str):
        try:
            parser = Parser(text)
            tokenizer = MinimalTokenizer(parser.parse())
            tokenizer.search_lexemes()

            # Mostrar ventana emergente con el resumen y las tablas
            summary_window = SummaryWindow(role, tokenizer)
            summary_window.exec_()

            # Mostrar texto en el área de texto principal
            self.text_display.clear()
            self.text_display.insertPlainText(text)

        except ValueError as ve:
            # Captura el ValueError y muestra el mensaje de error
            QMessageBox.critical(self, 'Error', f'Error de valor: {str(ve)}')

    def open_dialog(self):
        dialog = AddLexeme()
        if dialog.exec_() == dialog.Accepted:
            lexeme = dialog.get_data()
            if lexeme:
                FileManager.update_lexicon(lexeme)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
