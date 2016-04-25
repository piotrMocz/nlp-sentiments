import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from os import listdir, getcwd
from os.path import isfile, join, splitext
import file_utils


def word_feats(filename):
    """
    Constructs a bag-of-words representation of a file.
    :param words: List of words in a document.
    :return: Dict with a True entry for every distinct word in the text.
    """
    words = file_utils.get_words_from_file(filename)
    return dict([(word, True) for word in words])


def load_filenames(dir_path):
    """
    Scans through the files in the directory to extract the info from filenames
    :param dir_path: directory to scan
    :return: list of dicts containing info about the files
    """
    def strip_ext(filename):
        return splitext(filename)[0]

    def parse_tags(filename):
        bill_id, spkr_id, _, PMV = strip_ext(filename).split('_')
        party, mention_type, vote = PMV
        vote_bool = (vote == 'Y')
        return {'bill_id': int(bill_id),
                'spkr_id': int(spkr_id),
                'party': party,
                'mention_type': mention_type,
                'vote': vote_bool,
                'filename': filename}

    filenames = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    file_tags = [parse_tags(fname) for fname in filenames]

    return file_tags


def filter_feats(infos, feat_type):
    """
    Returns only the entries with a "Y" or "N" vote
    :param infos: List of dictionaries returned by `load_filenames`.
    :param feat_type: Vote type: "Y" or "N"
    :return: Filtered list of entries.
    """
    filter_fun = lambda info: info['vote'] if feat_type == 'pos' else not info['vote']
    return filter(filter_fun, infos)


# print 'Current directory: ' + getcwd()
#
# DIR_PREFIX = '/train_data/training_set/'
# DIR_FULL = getcwd() + DIR_PREFIX
# file_info = load_filenames(DIR_FULL)
# print 'Sample entry:'
# print file_info[0]
#
# print 'Finding negative ids...'
# negids = filter_feats(file_info, 'neg')
# print 'Sample negative id:'
# print negids[0]
#
# print 'Finding positive features...'
# posids = filter_feats(file_info, 'pos')
# print 'Sample positive id:'
# print posids[0]
#
# print 'Extracting negative features...'
# negfeats = [(word_feats(join(DIR_FULL, info['filename'])), 'neg') for info in negids]
# print 'Sample negative feature:'
# print negfeats[0]
#
# print 'Extracting positive features...'
# posfeats = [(word_feats(join(DIR_FULL, info['filename'])), 'pos') for info in posids]
# print 'Sample positive feature:'
# print posfeats[0]


# negids = movie_reviews.fileids('neg')
# posids = movie_reviews.fileids('pos')
#
# negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
# posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
#
# negcutoff = len(negfeats) * 3 / 4
# poscutoff = len(posfeats) * 3 / 4
#
# trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
# testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
# print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
#
# classifier = NaiveBayesClassifier.train(trainfeats)
# print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
# classifier.show_most_informative_features()
