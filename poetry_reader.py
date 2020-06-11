"""Functions for reading the pronouncing dictionary and the poetry forms files
"""
from typing import TextIO

from poetry_constants import (
    # CLEAN_POEM, WORD_PHONEMES, LINE_PRONUNCIATION, POEM_PRONUNCIATION,
    PRONOUNCING_DICTIONARY, POETRY_FORM, POETRY_FORMS)

SAMPLE_POETRY_FORM_FILE = '''Limerick
8 A
8 A
5 B
5 B
8 A

Haiku
5 *
7 * 
5 *
'''
EXPECTED_POETRY_FORMS = {
    'Haiku': ([5, 7, 5], ['*', '*', '*']),
    'Limerick': ([8, 8, 5, 5, 8], ['A', 'A', 'B', 'B', 'A'])
}

SAMPLE_DICTIONARY_FILE = ''';;; Comment line
ABSINTHE  AE1 B S IH0 N TH
HEART  HH AA1 R T
FONDER  F AA1 N D ER0
'''

EXPECTED_DICTIONARY = {
    'ABSINTHE': ['AE1', 'B', 'S', 'IH0', 'N', 'TH'],
    'HEART': ['HH', 'AA1', 'R', 'T'],
    'FONDER': ['F', 'AA1', 'N', 'D', 'ER0']
}

SAMPLE_POEM_FILE = '''  Is this mic on?

Get off my lawn.
'''


def read_and_trim_whitespace(poem_file: TextIO) -> str:
    """Return a string containing the poem in poem_file, with
     blank lines and leading and trailing whitespace removed.

     >>> poem_file = io.StringIO(SAMPLE_POEM_FILE)
     >>> read_and_trim_whitespace(poem_file)
     'Is this mic on?\\nGet off my lawn.'
     """
    lines = poem_file.readlines()
    poem = ''
    for line in lines:
        trimmed = line.strip()
        if trimmed == '':
            continue
        poem += trimmed + '\n'
    poem = poem[:-1]
    return poem


def read_pronouncing_dictionary(
        pronunciation_file: TextIO) -> PRONOUNCING_DICTIONARY:
    """Read pronunciation_file, which is in the format of the CMU Pronouncing
    Dictionary, and return the pronunciation dictionary.

    >>> dict_file = io.StringIO(SAMPLE_DICTIONARY_FILE)
    >>> result = read_pronouncing_dictionary(dict_file)
    >>> result == EXPECTED_DICTIONARY
    True
    """
    dictionary = {}
    lines = pronunciation_file.readlines()
    for line in lines:
        stripped = line.split()
        if stripped[0] == ';;;':
            continue
        dictionary[stripped[0]] = []
        for p in stripped[1:]:
            dictionary[stripped[0]].append(p)
    return dictionary

def read_poetry_form_descriptions(
        poetry_forms_file: TextIO) -> POETRY_FORMS:
    """Return a dictionary of poetry form name to poetry pattern for the poetry
    forms in poetry_forms_file.

    >>> form_file = io.StringIO(SAMPLE_POETRY_FORM_FILE)
    >>> result = read_poetry_form_descriptions(form_file)
    >>> result == EXPECTED_POETRY_FORMS
    True
    """
    line = poetry_forms_file.readline()
    types = {}
    while line:
        line = line.strip()
        types[line] = ([], [])
        new_line = poetry_forms_file.readline()
        while new_line.strip() != '':    
            splitted = new_line.split()
            types[line][0].append(int(splitted[0]))
            types[line][1].append(splitted[1])
            new_line = poetry_forms_file.readline()
        line = poetry_forms_file.readline()
    return types

if __name__ == "__main__":
    import doctest
    import io
    doctest.testmod()