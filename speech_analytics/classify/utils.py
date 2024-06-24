import re


def extract_and_remove_substring(sentence, substrings):
    found_substrings = []
    modified_sentence = sentence

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

    return found_substrings, modified_sentence.strip('_')


if __name__ == '__main__':
    # Ejemplo de uso
    sentence = "buen_dia_como_estás_en_esta_dia_como"
    substrings = ["buen_dia", "como", "no_estás"]

    found, final_modified_sentence = extract_and_remove_substring(sentence, substrings)

    if found:
        print(f"Subcadenas encontradas: {found}")
        print(f"Oración final modificada: '{final_modified_sentence}'")
    else:
        print("Ninguna de las subcadenas fue encontrada en la oración.")
