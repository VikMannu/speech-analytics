import json
from typing import Dict, Any, Optional

from speech_analytics.models.token_type import TokenType
from speech_analytics.models.word_info import WordInfo


class ReadFile:

    @staticmethod
    def read_json(file_path: str) -> Optional[Dict[str, WordInfo]]:
        """Lee un archivo JSON y devuelve un diccionario."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                word_info_dict = {
                    key: WordInfo(token=TokenType(value["token"]), weight=value["weight"])
                    for key, value in data.items()
                }
                return word_info_dict
        except (FileNotFoundError, IOError) as e:
            print(f"Error al leer el archivo: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error al parsear el archivo JSON: {e}")
            return None

    @staticmethod
    def update_data(data: Dict[str, Dict[str, Any]], key_to_update: str, new_value: Dict[str, Any]) -> Dict[
        str, Dict[str, Any]]:
        """Actualiza un elemento en el diccionario basado en la clave proporcionada."""
        data[key_to_update] = new_value
        return data

    @staticmethod
    def write_json(file_path: str, data: Dict[str, Dict[str, Any]]):
        """Escribe el diccionario en un archivo JSON."""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except (FileNotFoundError, IOError) as e:
            print(f"Error al leer el archivo: {e}")
        except json.JSONDecodeError as e:
            print(f"Error al parsear el archivo JSON: {e}")

    @classmethod
    def read_farewells(cls) -> Optional[Dict[str, WordInfo]]:
        return cls.read_json('../../data/farewells.json')

    @classmethod
    def read_greetings(cls) -> Optional[Dict[str, WordInfo]]:
        return cls.read_json('../../data/greetings.json')

    @classmethod
    def read_phrases(cls) -> Optional[Dict[str, WordInfo]]:
        return cls.read_json('../../data/phrases.json')

    @classmethod
    def read_words(cls) -> Optional[Dict[str, WordInfo]]:
        return cls.read_json('../../data/words.json')
