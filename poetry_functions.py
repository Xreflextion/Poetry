"""Helper functions for the poetry.py program.
"""

from typing import List
from typing import Tuple
from typing import Dict

from poetry_constants import (
    CLEAN_POEM, WORD_PHONEMES, LINE_PRONUNCIATION, POEM_PRONUNCIATION,
    PRONOUNCING_DICTIONARY)


# ===================== Helper Functions =====================


def clean_word(s: str) -> str:
    """Return a new string based on s in which all letters have been converted
    to uppercase and whitespace and punctuation characters have been stripped
    from both ends. Inner punctuation and whitespace is left untouched.

    >>> clean_word('Birthday!!!')
    'BIRTHDAY'
    >>> clean_word('  "Quoted?"\\n\\n\\n')
    'QUOTED'
    """

    punctuation = """!"'`@$%^&_-+={}|\\/,;:.-?)([]<>*#\n\t\r """
    result = s.upper().strip(punctuation)
    return result


def clean_poem(raw_poem: str) -> CLEAN_POEM:
    """Return the non-blank, non-empty lines of poem, with whitespace removed
    from the beginning and end of each line and all words capitalized.

    >>> clean_poem('The first line leads off,\\n\\n\\nWith a gap before the next.\\n    Then the poem ends.\\n')
    [['THE', 'FIRST', 'LINE', 'LEADS', 'OFF'], ['WITH', 'A', 'GAP', 'BEFORE', 'THE', 'NEXT'], ['THEN', 'THE', 'POEM', 'ENDS']]
    """
    raw_poem = raw_poem.split('\n')
    cleaned = []
    for line in raw_poem:
        words = line.strip().split()
        if words == []:
            continue
        cleaned.append([])
        for word in words:
            clean = clean_word(word)
            cleaned[-1].append(clean)
    return cleaned


def extract_phonemes(
        cleaned_poem: CLEAN_POEM,
        word_to_phonemes: PRONOUNCING_DICTIONARY) -> POEM_PRONUNCIATION:
    """Return a list where each inner list contains the phonemes for the
    corresponding line of poem_lines.

    >>> word_to_phonemes = {'YES': ['Y', 'EH1', 'S'], 'NO': ['N', 'OW1']}
    >>> extract_phonemes([['YES'], ['NO', 'YES']], word_to_phonemes)
    [[['Y', 'EH1', 'S']], [['N', 'OW1'], ['Y', 'EH1', 'S']]]
    """
    poem_pronunciation = []
    for line in cleaned_poem:
        poem_pronunciation.append([])
        for word in line:
            poem_pronunciation[-1].append(word_to_phonemes[word])
    return poem_pronunciation


def phonemes_to_str(poem_pronunciation: POEM_PRONUNCIATION) -> str:
    """Return a string containing all the phonemes in each word in each line in
    poem_pronunciation. The phonemes are separated by spaces, the words are
    separated by ' | ', and the lines are separated by '\n'.

    >>> phonemes_to_str([[['Y', 'EH1', 'S']], [['N', 'OW1'], ['Y', 'EH1', 'S']]])
    'Y EH1 S\\nN OW1 | Y EH1 S'
    """
    pronunciation = ''
    for line in poem_pronunciation:
        for word in line:
            word = ' '.join(word)
            pronunciation += word + ' | '
        pronunciation = pronunciation[:-3]
        pronunciation += '\n'
    return pronunciation[:-1]


def get_rhyme_scheme(poem_pronunciation: POEM_PRONUNCIATION) -> List[str]:
    """Return a list of last syllables from the poem described by
    poem_pronunction.

    Precondition: poem_pronunciation is not empty and each PHONEMES list
    contains at least one vowel phoneme.

    >>> get_rhyme_scheme([[['IH0', 'N']], [['S', 'IH0', 'N']]])
    ['A', 'A']
    """
    letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    idx = 0
    check = {}
    rhyme = []
    for line in poem_pronunciation:
        last = line[-1]
        last_syllables = []
        for p in last[::-1]:
            last_syllables.append(p)
            if p[-1].isdigit():
                break
        last_syllables.reverse()
        last_syllables = ''.join(last_syllables)
        if last_syllables in check:
            rhyme.append(check[last_syllables])
        else:
            rhyme.append(letter[idx])
            check[last_syllables] = letter[idx]
            idx += 1
    return rhyme


def get_num_syllables(poem_pronunciation: POEM_PRONUNCIATION) -> List[int]:
    """Return a list of the number of syllables in each poem_pronunciation
    line.
    >>> get_num_syllables([[['IH0', 'N']], [['S', 'IH0', 'N']]])
    [1, 1]
    """
    num_syllables = []
    for line in poem_pronunciation:
        num = 0
        for word in line:
            for p in word:
                if p[-1].isdigit():
                    num += 1
        num_syllables.append(num)
    return num_syllables


if __name__ == '__main__':
    import doctest

    doctest.testmod()
