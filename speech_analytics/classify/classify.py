import re
from collections import defaultdict
from typing import List, Optional, Dict

from speech_analytics.models.word_info import WordInfo
from speech_analytics.read_file.read_file import ReadFile


class Classify:
    def __init__(self, sentence):
        self.sentence = sentence
        self.filtered_sentence = sentence
        self.greetings: Optional[Dict[str, WordInfo]] = ReadFile.read_greetings()
        self.greetings_keys: Optional[defaultdict[int]] = None
        self.farewells: Optional[Dict[str, WordInfo]] = ReadFile.read_farewells()
        self.farewells_keys: Optional[defaultdict[int]] = None
        self.phrases: Optional[Dict[str, WordInfo]] = ReadFile.read_phrases()
        self.phrases_keys: Optional[defaultdict[int]] = None
        self.words: Optional[Dict[str, WordInfo]] = ReadFile.read_words()
        self.words_keys: Optional[defaultdict[int]] = None

    def extract_and_remove_substring(self, substrings: List[str]):
        found_substrings = defaultdict(int)
        modified_sentence = self.sentence

        for substring in substrings:
            # Creamos una expresión regular para buscar la subcadena
            regex = re.compile(r'(' + re.escape(substring) + r')')

            # Buscamos la subcadena en la oración
            matches = regex.findall(modified_sentence)

            if matches:
                for match in matches:
                    # Añadimos todas las coincidencias encontradas
                    found_substrings[match] += 1

                    # Removemos todas las subcadenas encontradas del original
                modified_sentence = regex.sub('', modified_sentence)

        # Eliminamos los guiones bajos adicionales
        self.filtered_sentence = re.sub(r'_{2,}', '_', modified_sentence).strip('_')

        return found_substrings

    def classify(self):
        self.greetings_keys = self.extract_and_remove_substring(list(self.greetings.keys()))
        self.farewells_keys = self.extract_and_remove_substring(list(self.farewells.keys()))
        self.phrases_keys = self.extract_and_remove_substring(list(self.phrases.keys()))
        self.words_keys = self.extract_and_remove_substring(list(self.words.keys()))
