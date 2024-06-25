from collections import deque
from typing import List, Optional, Tuple

from speech_analytics.file_manager.file_manager import FileManager, Lexicon
from speech_analytics.models.lexeme import Lexeme
from speech_analytics.models.token_type import TokenType


class MinimalTokenizer:
    def __init__(self, sentence: List[str]):
        self.sentence = sentence
        self.lexicon: Lexicon = FileManager.read_lexicon()
        self.tokenized_lexemes: List[Lexeme] = []
        self.non_tokenized_lexemes: List[str] = []
        self.token_types_found: set[TokenType] = set()

    @property
    def evaluation(self) -> Tuple[str, float]:
        good_sum, bad_sum, greeting_weight, farewell_weight = self.__categorize_and_sum_weights()
        normalized_good, normalized_bad, normalized_greeting, normalized_farewell = self.__normalize_weights(good_sum, bad_sum, greeting_weight, farewell_weight)
        score = self.__final_evaluation(normalized_good, normalized_bad, normalized_greeting, normalized_farewell)
        return self.__map_score_to_category(score), score

    def __categorize_and_sum_weights(self) -> Tuple[int, int, int, int]:
        good_sum = 0
        bad_sum = 0
        greeting_weight = 0
        farewell_weight = 0
        for lexeme in self.tokenized_lexemes:
            if lexeme.token == TokenType.GOOD:
                good_sum += lexeme.weight
            elif lexeme.token == TokenType.BAD:
                bad_sum += lexeme.weight
            elif lexeme.token == TokenType.GREETING:
                greeting_weight += lexeme.weight
            elif lexeme.token == TokenType.FAREWELL:
                farewell_weight += lexeme.weight
        return good_sum, bad_sum, greeting_weight, farewell_weight

    @staticmethod
    def __normalize_weights(good_sum: int, bad_sum: int, greeting_weight: int, farewell_weight: int) -> Tuple[float, float, float, float]:
        total = good_sum + bad_sum + greeting_weight + farewell_weight
        if total == 0:
            return 0.0, 0.0, 0.0, 0.0  # Avoid division by zero
        normalized_good = good_sum / total
        normalized_bad = bad_sum / total
        normalized_greeting_weight = greeting_weight / total
        normalized_farewell_weight = farewell_weight / total
        return normalized_good, normalized_bad, normalized_greeting_weight, normalized_farewell_weight

    def __final_evaluation(self, normalized_good: float, normalized_bad: float, normalized_greeting: float, normalized_farewell: float) -> float:
        if not self.has_greeting:
            normalized_greeting += 0.05  # Adjust bad score if greeting is missing
        else:
            normalized_greeting -= 0.1

        if not self.has_farewell:
            normalized_farewell += 0.05  # Adjust bad score if farewell is missing
        else:
            normalized_farewell -= 0.1

        return normalized_good - normalized_bad + normalized_greeting + normalized_farewell

    @staticmethod
    def __map_score_to_category(score: float) -> str:
        if score <= -0.5:
            return 'MUY_MALAS'
        elif -0.5 < score <= -0.1:
            return 'MALAS'
        elif -0.1 < score <= 0.1:
            return 'NEUTRAS'
        elif 0.1 < score <= 0.5:
            return 'BUENAS'
        else:
            return 'MUY_BUENAS'

    def search_lexemes(self):
        sentence_to_map = deque(self.sentence)
        while sentence_to_map:
            word = sentence_to_map[0]
            if word in self.lexicon:
                lexemes = list(self.lexicon[word].values())
                lexeme = self.__search_best_match(list(sentence_to_map), lexemes)
                if lexeme:
                    self.tokenized_lexemes.append(lexeme)
                    self.token_types_found.add(lexeme.token)
                    for _ in range(lexeme.length):
                        sentence_to_map.popleft()
                else:
                    self.non_tokenized_lexemes.append(sentence_to_map.popleft())
            else:
                self.non_tokenized_lexemes.append(sentence_to_map.popleft())

    def __search_best_match(self, sentence_to_map: List[str], lexemes: List[Lexeme]) -> Optional[Lexeme]:
        sentence = '_'.join(sentence_to_map)
        search_results: List[Lexeme] = [
            lexeme for lexeme in lexemes if self.__is_present_in_order(lexeme.key, sentence)
        ]

        return max(search_results, key=lambda lexeme: lexeme.length, default=None)

    @staticmethod
    def __is_present_in_order(str1: str, str2: str) -> bool:
        return str2.startswith(str1)

    @property
    def has_greeting(self) -> bool:
        return TokenType.GREETING in self.token_types_found

    @property
    def has_farewell(self) -> bool:
        return TokenType.FAREWELL in self.token_types_found
