import re
from typing import Optional, Dict

from speech_analytics.read_file.read_file import ReadFile, WordInfo


class Classify:
    def __init__(self, sentence):
        self.sentence = sentence
        self.filtered_sentence = sentence
        self.greetings: Optional[Dict[str, WordInfo]] = ReadFile.read_greetings()
        self.greetings_keys = None
        self.farewells: Optional[Dict[str, WordInfo]] = ReadFile.read_farewells()
        self.farewells_keys = None
        self.phrases: Optional[Dict[str, WordInfo]] = ReadFile.read_phrases()
        self.phrases_keys = None
        self.words: Optional[Dict[str, WordInfo]] = ReadFile.read_words()
        self.words_keys = None

    def extract_and_remove_substring(self, substrings):
        found_substrings = []
        modified_sentence = self.sentence

        for substring in substrings:
            # Creamos una expresión regular para buscar la subcadena
            regex = re.compile(r'(' + re.escape(substring) + r')')

            # Buscamos la subcadena en la oración
            match = regex.search(modified_sentence)

            if match:
                # Extraemos la subcadena encontrada
                extracted_substring = match.group(1)
                found_substrings.append(extracted_substring)

                # Removemos la subcadena encontrada del original
                modified_sentence = regex.sub('', modified_sentence)

            self.filtered_sentence = re.sub(r'_{2,}', '_', modified_sentence).strip('_')
        return found_substrings

    def classify(self):
        self.greetings_keys = self.extract_and_remove_substring(list(self.greetings.keys()))
        self.farewells_keys = self.extract_and_remove_substring(self.farewells.keys())
        self.phrases_keys = self.extract_and_remove_substring(self.phrases.keys())
        self.words_keys = self.extract_and_remove_substring(list(self.words.keys()))
