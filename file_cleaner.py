__author__ = 'Michal'

import time
import re
from os import listdir, getcwd, path

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from data_loader import load_filenames, filter_feats
from db_manager import DBManager
from config import DIR_FILES, DIR_CLEANED_FILES
from file_utils import create_dir


manager = DBManager()
manager.create()
stemmer = SnowballStemmer("english")
VERBOSE = True


def clean_word(w):
    """
    Delete all the redundant information encoded in a word.
    :param w: word to be cleaned
    :return: cleaned word
    """
    if w in [".", "?", "!"]: # will be needed for ngrams to find out where a sentence finishes.
        return w
    w = w.lower()
    w = re.sub('[^A-Za-z]+', '', w)
    if w in stopwords.words('english'):
        return None

    word = stemmer.stem(w).encode('ascii', 'english')
    return word if word != '' else None


def clean_and_write_speeches(fileinfos):
    """
    Go through files represented by dictionaries, create a record for each in the db, and save clean version of it[file].
    :param fileinfos:
    :return:
    """
    create_dir(DIR_CLEANED_FILES)

    pos_vote_chunk = fileinfos[0]["vote"]
    for curr_file in fileinfos:
        success = manager.insert_speech(filename=curr_file["filename"],
                                        vote=pos_vote_chunk,
                                        party=curr_file["party"],
                                        mention_type=curr_file["mention_type"])
        if success:
            new_file_content = ""
            cleaned_file = path.join(DIR_CLEANED_FILES, curr_file["filename"])
            base_file = path.join(".", DIR_FILES, curr_file["filename"])
            with open(cleaned_file, "w+") as writeH:
                with open(base_file, "r") as readH:
                    for line in readH:
                        for word in line.split():
                            cleanWord = clean_word(word)
                            if cleanWord:
                                new_file_content += cleanWord + " "

                    writeH.seek(0)
                    writeH.write(new_file_content)
                    writeH.truncate()

        else:
            print "db error while saving {0}".format(curr_file)


if __name__ == "__main__":
    start = time.time()

    DIR_PREFIX = '/train_data/training_set/'
    DIR_FULL = getcwd() + DIR_PREFIX
    file_info = load_filenames(DIR_FULL)

    negids = filter_feats(file_info, 'neg')
    print 'Sample negative id:'
    print negids[0]
    print "nr of negative ids: {0}".format(len(negids))
    print 'Finding positive features...'
    posids = filter_feats(file_info, 'pos')
    print "nr of positive ids: {0}".format(len(posids))

    clean_and_write_speeches(posids)
    clean_and_write_speeches(negids)

    stop = time.time()
    print "Time spent: ", stop-start