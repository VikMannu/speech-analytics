import tkinter as tk
from tkinter import filedialog, Text

from speech_analytics.bnf.parser import Parser
from speech_analytics.classify.classify import Classify


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Analytics")

        # Crear un botón para abrir el archivo
        self.open_button = tk.Button(root, text="Abrir Archivo", command=self.open_file)
        self.open_button.pack(pady=10)

        # Crear un área de texto para mostrar el contenido del archivo
        self.text_display = Text(root, wrap=tk.WORD, width=80, height=20)
        self.text_display.pack(padx=10, pady=10)

    def open_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return

        with open(filepath, "r") as file:
            text = file.read()

        parser = Parser(text)
        classify = Classify(parser.parse())
        classify.classify()
        self.display_results(text, classify)

    def display_results(self, text, classify):
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, text)
        # Configurar el tag "white" para que el texto sea blanco
        self.text_display.tag_configure("white", foreground="white")
        self.text_display.insert(tk.END, "\n\n--- Resumen ---\n")
        self.text_display.insert(tk.END, f"Saludos: {', '.join(classify.greetings_keys)}\n")
        self.text_display.insert(tk.END, f"Despedidas: {', '.join(classify.farewells_keys)}\n")
        self.text_display.insert(tk.END, f"Frases: {', '.join(classify.phrases_keys)}\n")
        self.text_display.insert(tk.END, f"Palabras encontradas: {', '.join(classify.words)}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
