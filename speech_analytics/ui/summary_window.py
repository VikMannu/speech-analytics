from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QTableWidget, QVBoxLayout, QHeaderView, QTableWidgetItem

from speech_analytics.minimal_tokenizer.minimal_tokenizer import MinimalTokenizer
from speech_analytics.models.lexeme import Lexeme
from speech_analytics.models.role import Role


class SummaryWindow(QDialog):
    def __init__(self, role: Role, tokenizer: MinimalTokenizer):
        super().__init__()

        self.setWindowTitle(f"Resumen para {role.title}")
        self.setMinimumWidth(600)

        self.role_label = QLabel(f"Resumen para {role.title}")
        self.role_label.setAlignment(Qt.AlignCenter)

        self.summary_label = QLabel()
        self.setup_summary(role, tokenizer)

        self.tokenized_table = QTableWidget()
        self.setup_tokenized_table(tokenizer.tokenized_lexemes)

        self.non_tokenized_table = QTableWidget()
        self.setup_non_tokenized_table(tokenizer.non_tokenized_lexemes)

        layout = QVBoxLayout()
        layout.addWidget(self.role_label)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.tokenized_table)
        layout.addWidget(self.non_tokenized_table)

        self.setLayout(layout)

    def setup_summary(self, role: Role, tokenizer: MinimalTokenizer):
        summary_text = "--- Resumen ---\n"
        summary_text += f"\nEvaluación:\n"

        if role == Role.AGENT:
            if tokenizer.has_greeting:
                summary_text += f"Contiene saludo\n"
            else:
                summary_text += f"NO contiene saludo\n"

            if tokenizer.has_farewell:
                summary_text += f"Contiene despedida\n"
            else:
                summary_text += f"NO contiene despedida\n"

            if tokenizer.has_identification:
                summary_text += f"Contiene identificación\n"
            else:
                summary_text += f"NO contiene identificación\n"

        message, score = tokenizer.evaluation
        summary_text += f"Evaluación final: {message} ({score})\n"

        self.summary_label.setText(summary_text)

    def setup_tokenized_table(self, tokenized_lexemes: List[Lexeme]):
        self.tokenized_table.setColumnCount(3)
        self.tokenized_table.setHorizontalHeaderLabels(['Lexemas', 'Peso', 'Tipo de Token'])
        self.tokenized_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tokenized_table.setRowCount(len(tokenized_lexemes))

        for row, lexeme in enumerate(tokenized_lexemes):
            self.tokenized_table.setItem(row, 0, QTableWidgetItem(' '.join(lexeme.lexemes)))
            self.tokenized_table.setItem(row, 1, QTableWidgetItem(str(lexeme.weight)))
            self.tokenized_table.setItem(row, 2, QTableWidgetItem(str(lexeme.token.title)))

    def setup_non_tokenized_table(self, non_tokenized_lexemes):
        self.non_tokenized_table.setColumnCount(1)
        self.non_tokenized_table.setHorizontalHeaderLabels(['Palabras No Tokenizadas'])
        self.non_tokenized_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.non_tokenized_table.setRowCount(len(non_tokenized_lexemes))

        for row, word in enumerate(non_tokenized_lexemes):
            print(word)
            self.non_tokenized_table.setItem(row, 0, QTableWidgetItem(word))
