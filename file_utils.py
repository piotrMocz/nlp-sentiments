import re
from os import path, makedirs


def get_words_from_string(s, as_set=True):
    words = re.findall(re.compile('\w+'), s.lower())
    return set(words) if as_set else words


def get_words_from_file(fname, as_set=True):
    with open(fname, 'rb') as inf:
        return get_words_from_string(inf.read(), as_set)


def create_dir(dirpath):
    if not path.exists(dirpath):
        makedirs(dirpath)
