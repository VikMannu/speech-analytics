from collections import deque
from typing import List, Optional, Dict

from speech_analytics.file_manager.file_manager import FileManager, Lexicon
from speech_analytics.models.lexeme import Lexeme
from speech_analytics.models.token_type import TokenType


class MinimalTokenizer:
    def __init__(self, sentence: List[str]):
        self.sentence = sentence
        self.lexicon: Lexicon = FileManager.read_lexicon()
        self.lexemes_found: List[Lexeme] = []
        self.lexemes_not_found: List[str] = []
        self.token_types_found: set[TokenType] = set()

    def search_lexemes(self):
        sentence_to_map = deque(self.sentence)
        while sentence_to_map:
            word = sentence_to_map[0]
            if word in self.lexicon:
                lexemes = self.lexicon[word]
                lexeme = self.__search_best_match(list(sentence_to_map), lexemes)
                if lexeme:
                    self.lexemes_found.append(lexeme)
                    self.token_types_found.add(lexeme.token)
                    for _ in range(lexeme.length):
                        sentence_to_map.popleft()
                else:
                    self.lexemes_not_found.append(sentence_to_map.popleft())
            else:
                self.lexemes_not_found.append(sentence_to_map.popleft())

    def __search_best_match(self, sentence_to_map: List[str], lexemes: List[Lexeme]) -> Optional[Lexeme]:
        search_results: List[Lexeme] = [
            lexeme for lexeme in lexemes if self.__is_present_in_order(lexeme.lexemes, sentence_to_map)
        ]

        return max(search_results, key=lambda lexeme: lexeme.length, default=None)

    @staticmethod
    def __is_present_in_order(list1: List[str], list2: List[str]) -> bool:
        str_list1 = ' '.join(list1)
        str_list2 = ' '.join(list2)
        return str_list2.startswith(str_list1)

    @property
    def has_greeting(self) -> bool:
        return TokenType.GREETING in self.token_types_found

    @property
    def has_farewell(self) -> bool:
        return TokenType.FAREWELL in self.token_types_found
