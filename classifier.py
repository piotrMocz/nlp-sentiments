from os.path import join

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

import file_utils
import db_manager
from config import DIR_CLEANED_FILES

db = db_manager.DBManager()


def word_feats(filename):
    """
    Constructs a bag-of-words representation of a file.
    :param words: List of words in a document.
    :return: Dict with a True entry for every distinct word in the text.
    """
    full_name = join(DIR_CLEANED_FILES, filename)
    words = file_utils.get_words_from_file(full_name)
    return dict([(word, True) for word in words])


def load_feats(vote):
    file_infos = db.get_infos(count=None, vote=vote)
    pos = 'pos' if vote == 'T' else 'neg'
    return [(word_feats(fi['filename']), pos) for fi in file_infos]


if __name__ == '__main__':
    neg_feats = load_feats('F')
    pos_feats = load_feats('T')

    neg_cutoff = len(neg_feats) * 3 / 4
    pos_cutoff = len(pos_feats) * 3 / 4

    train_feats = neg_feats[:neg_cutoff] + pos_feats[:pos_cutoff]
    test_feats = neg_feats[neg_cutoff:] + pos_feats[pos_cutoff:]
    print 'Train on %d instances, test on %d instances' % (len(train_feats), len(test_feats))

    classifier = NaiveBayesClassifier.train(train_feats)
    print 'Accuracy:', nltk.classify.util.accuracy(classifier, test_feats)
    classifier.show_most_informative_features()
