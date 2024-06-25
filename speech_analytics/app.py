import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QMessageBox

from speech_analytics.bnf.parser import Parser
from speech_analytics.minimal_tokenizer.minimal_tokenizer import MinimalTokenizer


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speech Analytics")

        # Crear un botón para abrir el archivo
        self.open_button = QPushButton("Abrir Archivo", self)
        self.open_button.clicked.connect(self.open_file)

        # Crear un área de texto para mostrar el contenido del archivo
        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.text_display.setLineWrapMode(QTextEdit.WidgetWidth)
        self.text_display.setFixedSize(800, 400)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
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
            text = file.read()

        try:
            parser = Parser(text)
            minimal_tokenizer = MinimalTokenizer(parser.parse())
            minimal_tokenizer.search_lexemes()
            self.display_results(text, minimal_tokenizer)
        except ValueError as ve:
            # Captura el ValueError y muestra el mensaje de error
            QMessageBox.critical(self, 'Error', f'Error de valor: {str(ve)}')

    def display_results(self, text: str, minimal_tokenizer: MinimalTokenizer):
        self.text_display.clear()
        self.text_display.insertPlainText(text)
        self.text_display.insertPlainText("\n\n--- Resumen ---\n")
        self.text_display.insertPlainText(f"Palabras encontradas:\n")
        for lexeme in minimal_tokenizer.lexemes_found:
            self.text_display.insertPlainText(f"{lexeme}\n")

        self.text_display.insertPlainText(f"\nPalabras no encontradas:\n")
        for word in minimal_tokenizer.lexemes_not_found:
            self.text_display.insertPlainText(f"{word}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
