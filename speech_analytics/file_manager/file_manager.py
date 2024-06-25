import json
import os
from typing import Dict, List, TypeAlias, Optional

from speech_analytics.models.lexeme import Lexeme
from speech_analytics.models.token_type import TokenType

Lexicon: TypeAlias = Dict[str, Dict[str, Lexeme]]


class FileManager:

    @staticmethod
    def read_json(file_path: str):
        """Lee un archivo JSON y devuelve un diccionario."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, IOError) as e:
            print(f"Error al leer el archivo: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error al parsear el archivo JSON: {e}")
            return None

    @staticmethod
    def write_json(file_path: str, data):
        """Escribe el diccionario en un archivo JSON."""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except (FileNotFoundError, IOError) as e:
            print(f"Error al leer el archivo: {e}")
        except json.JSONDecodeError as e:
            print(f"Error al parsear el archivo JSON: {e}")

    @classmethod
    def read_lexicon(cls) -> Optional[Lexicon]:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, '../../data/lexicon.json')
        data = cls.read_json(file_path)
        lexicon: Lexicon = {}
        for key, value in data.items():
            lexemes = {}
            for lexeme_key, item in value.items():  # iterate over values in the nested dictionary
                lexeme = Lexeme(
                    lexemes=item['lexemes'],
                    token=TokenType[item['token']],
                    weight=item['weight']
                )
                lexemes[lexeme_key] = lexeme
            lexicon[key] = lexemes

        return lexicon

    @classmethod
    def update_lexicon(cls, lexicon: Dict[str, List[Lexeme]]):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, '../../data/lexicon.json')
        cls.write_json(file_path, lexicon)
