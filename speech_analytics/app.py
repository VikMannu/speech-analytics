import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QMessageBox

from speech_analytics.bnf.parser import Parser
from speech_analytics.file_manager.file_manager import FileManager
from speech_analytics.minimal_tokenizer.minimal_tokenizer import MinimalTokenizer
from speech_analytics.ui.add_lexeme import AddLexeme


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speech Analytics")

        self.text: str = ""

        # Botón para abrir el archivo
        self.open_button = QPushButton("Abrir Archivo", self)
        self.open_button.clicked.connect(self.open_file)

        # Botón para abrir el diálogo personalizado
        self.open_dialog_button = QPushButton("Agregar Lexema", self)
        self.open_dialog_button.clicked.connect(self.open_dialog)

        # Crear un área de texto para mostrar el contenido del archivo
        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.text_display.setLineWrapMode(QTextEdit.WidgetWidth)
        self.text_display.setFixedSize(800, 400)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.open_dialog_button)
        layout.addWidget(self.text_display)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo", "", "Text files (*.txt);;All files (*.*)")
        if not filepath:
            return

        with open(filepath, "r") as file:
            self.text = file.read()

        self.display_results()

    def display_results(self):
        try:
            parser = Parser(self.text)
            minimal_tokenizer = MinimalTokenizer(parser.parse())
            minimal_tokenizer.search_lexemes()
            self.text_display.clear()
            self.text_display.insertPlainText(self.text)
            self.text_display.insertPlainText("\n\n--- Resumen ---\n")
            self.text_display.insertPlainText(f"\nEvaluación:\n")
            if minimal_tokenizer.has_greeting:
                self.text_display.insertPlainText(f"Contiene saludo\n")
            else:
                self.text_display.insertPlainText(f"NO contiene saludo\n")

            if minimal_tokenizer.has_farewell:
                self.text_display.insertPlainText(f"Contiene despedida\n")
            else:
                self.text_display.insertPlainText(f"NO contiene despedida\n")

            message, score = minimal_tokenizer.evaluation
            self.text_display.insertPlainText(f"Evaluación final: {message}({score})\n")

            self.text_display.insertPlainText(f"\nPalabras tokenizadas:\n")
            for lexeme in minimal_tokenizer.tokenized_lexemes:
                self.text_display.insertPlainText(f"{lexeme}\n")

            self.text_display.insertPlainText(f"\nPalabras no tokenizadas:\n")
            for word in minimal_tokenizer.non_tokenized_lexemes:
                self.text_display.insertPlainText(f"{word}\n")
        except ValueError as ve:
            # Captura el ValueError y muestra el mensaje de error
            QMessageBox.critical(self, 'Error', f'Error de valor: {str(ve)}')

    def open_dialog(self):
        dialog = AddLexeme()
        if dialog.exec_() == dialog.Accepted:
            lexeme = dialog.get_data()
            if lexeme:
                FileManager.update_lexicon(lexeme)
                self.display_results()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
