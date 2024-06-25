import re
from collections import defaultdict
from typing import List, Optional, Dict

from speech_analytics.models.lexeme import Lexeme
from speech_analytics.read_file.read_file import ReadFile


class MinimalTokenizer:
    def __init__(self, sentence: List[str]):
        self.sentence = sentence
        self.lexicon = ReadFile.read_lexicon()
        self.lexemes_found: Optional[List[Lexeme]] = None
        self.lexemes_not_found: Optional[List[str]] = None

    def tokenize(self):
        print('Classifying...')
