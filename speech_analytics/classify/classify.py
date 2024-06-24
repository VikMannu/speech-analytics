import re
from typing import Optional, Dict

from speech_analytics.read_file.read_file import ReadFile, WordInfo


class Classify:
    def __init__(self, sentence):
        self.sentence = sentence
        self.greetings: Optional[Dict[str, WordInfo]] = ReadFile.read_greetings()
        self.farewells: Optional[Dict[str, WordInfo]] = ReadFile.read_farewells()
        self.phrases: Optional[Dict[str, WordInfo]] = ReadFile.read_phrases()
        self.words: Optional[Dict[str, WordInfo]] = ReadFile.read_words()

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

            self.sentence = re.sub(r'_{2,}', '_', modified_sentence).strip('_')
        return found_substrings

    def classify(self):
        greetings_keys = self.extract_and_remove_substring(list(self.greetings.keys()))
        farewells_keys = self.extract_and_remove_substring(self.farewells.keys())
        phrases_keys = self.extract_and_remove_substring(self.phrases.keys())
        words_keys = self.extract_and_remove_substring(list(self.words.keys()))

        print(farewells_keys)
        print(greetings_keys)
        print(phrases_keys)
        print(words_keys)
        print(self.sentence.split('_'))

        score = 0

        if greetings_keys:
            for greeting in greetings_keys:
                print(self.greetings[greeting])
                score = score + self.greetings[greeting].weight
                print(score)
        else:
            print('No se cumplió con los requisitos mínimos de saludo')

        if farewells_keys:
            for farewell in farewells_keys:
                score = score + self.farewells[farewell].weight
                print(score)
        else:
            print('No se cumplió con los requisitos mínimos de despedida')
