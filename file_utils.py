import re


def get_words_from_string(s):
    return set(re.findall(re.compile('\w+'), s.lower()))


def get_words_from_file(fname):
    with open(fname, 'rb') as inf:
        return get_words_from_string(inf.read())
