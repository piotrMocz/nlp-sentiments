import re
from os import path, makedirs

def get_words_from_string(s):
    return set(re.findall(re.compile('\w+'), s.lower()))


def get_words_from_file(fname):
    with open(fname, 'rb') as inf:
        return get_words_from_string(inf.read())


def create_dir(dirpath):
    if not path.exists(dirpath):
        makedirs(dirpath)
