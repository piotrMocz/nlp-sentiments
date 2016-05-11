import os
import config
import file_utils


def make_ngram_strings(fname, n):
    """
    Returns list of ngrams (as strings) for a given file.
    Strings are used to enable dict-based storage.
    :param fname: name of the file to read words from
    :param n: the rank of ngrams to create
    :return: dictionary: {ngram -> num of occurrences}
    """
    words = file_utils.get_words_from_file(fname, as_set=False)

    wcount = len(words)
    ngrams = {}

    for i in xrange(wcount - n + 1):
        ngram = ' '.join(words[i:i+n])

        if ngram in ngrams:
            ngrams[ngram] += 1
        else:
            ngrams[ngram] = 1

    return ngrams


def combine_ngrams_dicts(dict1, dict2):
    """"
    Combines two dictionaries with ngrams counts into one
    :param dict1 First dict
    :param dict2 Second dict
    :return dict with combined occurrence counts for ngrams
    """
    for ngram, cnt in dict2.iteritems():
        if ngram in dict1:
            dict1[ngram] += cnt
        else:
            dict1[ngram] = cnt

    return dict1


def get_all_ngrams(file_dir, n):
    """
    Returns all ngrams from files from a given directory
    :param file_dir: directory to read files from
    :param n: rank of ngrams to make
    :return: string-based dictionary of all ngrams in the directory
    """
    files = (os.path.join(file_dir, f) for f in os.listdir(file_dir) if os.path.isfile(os.path.join(file_dir, f)))
    ngram_dicts = (make_ngram_strings(f, n) for f in files)
    ngrams_dict = {}

    for ngd in ngram_dicts:
        ngrams_dict = combine_ngrams_dicts(ngd, ngrams_dict)

    return ngrams_dict


if __name__ == '__main__':
    f_dir = os.path.join('..', config.DIR_CLEANED_FILES)
    ngd = get_all_ngrams(f_dir, 2)
    for k, v in ngd.iteritems():
        print "{0}: {1}".format(k, v)
