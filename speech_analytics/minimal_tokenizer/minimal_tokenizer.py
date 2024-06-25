from typing import List, Optional

from speech_analytics.models.lexeme import Lexeme
from speech_analytics.read_file.read_file import ReadFile


class MinimalTokenizer:
    def __init__(self, sentence: List[str]):
        self.sentence = sentence
        self.lexicon = ReadFile.read_lexicon()
        self.lexemes_found: List[Lexeme] = []
        self.lexemes_not_found: List[str] = []

    def search_lexemes(self):
        sentence_to_map = self.sentence.copy()
        while sentence_to_map:
            word = sentence_to_map[0]
            if word in self.lexicon:
                lexemes = self.lexicon[word]
                lexeme = self.__search_matches(sentence_to_map, lexemes)
                self.lexemes_found.append(lexeme)
            else:
                self.lexemes_not_found = sentence_to_map.pop(0)

    def __search_matches(self, sentence_to_map: List[str], lexemes: List[Lexeme]) -> Lexeme:
        search_results: List[Lexeme] = []
        for lexeme in lexemes:
            if len(lexeme.lexemes) > 1:
                if self.__is_present_in_order(lexeme.lexemes, sentence_to_map):
                    search_results.append(lexeme)
            else:
                search_results.append(lexeme)

        return max(search_results, key=lambda lexeme: lexeme.length)

    @staticmethod
    def __is_present_in_order(list1: List[str], list2: List[str]) -> bool:
        # Convert both lists to strings to use startswith
        str_list1 = ' '.join(map(str, list1))
        str_list2 = ' '.join(map(str, list2))

        # Use startswith to check if list1 is at the beginning of list2
        return str_list2.startswith(str_list1)

    def tokenize(self):
        print('Classifying...')
