from typing import List, Optional

from speech_analytics.models.lexeme import Lexeme
from speech_analytics.file_manager.file_manager import FileManager
from speech_analytics.models.token_type import TokenType


class MinimalTokenizer:
    def __init__(self, sentence: List[str]):
        self.sentence = sentence
        self.lexicon = FileManager.read_lexicon()
        self.lexemes_found: List[Lexeme] = []
        self.lexemes_not_found: List[str] = []
        self.has_greeting: bool = False
        self.has_farewell: bool = False

    def search_lexemes(self):
        sentence_to_map = self.sentence.copy()
        while sentence_to_map:
            word = sentence_to_map[0]
            if word in self.lexicon:
                lexemes = self.lexicon[word]
                lexeme = self.__search_matches(sentence_to_map, lexemes)
                if lexeme is not None:
                    self.lexemes_found.append(lexeme)
                    if lexeme.token == TokenType.GREETING:
                        self.has_greeting = True
                    elif lexeme.token == TokenType.FAREWELL:
                        self.has_farewell = True
                    for _ in range(lexeme.length):
                        sentence_to_map.pop(0)
                else:
                    self.lexemes_not_found.append(sentence_to_map.pop(0))
            else:
                self.lexemes_not_found.append(sentence_to_map.pop(0))

    def __search_matches(self, sentence_to_map: List[str], lexemes: List[Lexeme]) -> Optional[Lexeme]:
        search_results: List[Lexeme] = []
        for lexeme in lexemes:
            if len(lexeme.lexemes) > 1:
                if self.__is_present_in_order(lexeme.lexemes, sentence_to_map):
                    search_results.append(lexeme)
            else:
                search_results.append(lexeme)

        if search_results:
            return max(search_results, key=lambda lexeme: lexeme.length)

        return None

    @staticmethod
    def __is_present_in_order(list1: List[str], list2: List[str]) -> bool:
        # Convert both lists to strings to use startswith
        str_list1 = ' '.join(map(str, list1))
        str_list2 = ' '.join(map(str, list2))

        # Use startswith to check if list1 is at the beginning of list2
        return str_list2.startswith(str_list1)
