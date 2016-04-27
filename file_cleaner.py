__author__ = 'Michal'

import time
from os import getcwd
from election_sentiments import load_filenames, filter_feats
from db_manager import DBManager
from config import DIR_FILES, DIR_CLEANED_FILES
import re

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

manager = DBManager()
stemmer = SnowballStemmer("english")
VERBOSE = True

def cleaningOfWord(wordBeingCleaned):
    """
    Delete all the redundant information encoded in a word.
    :param wordBeingCleaned: word to be cleaned
    :return: cleaned word
    """
    if wordBeingCleaned in [".", "?", "!"]: # will be needed for ngrams to find out where a sentence finishes.
        return wordBeingCleaned
    wordBeingCleaned = wordBeingCleaned.lower()
    wordBeingCleaned = re.sub('[^A-Za-z]+', '', wordBeingCleaned)
    if wordBeingCleaned in stopwords.words('english'):
        return None

    word = stemmer.stem(wordBeingCleaned).encode('ascii', 'english')
    return word if word != '' else None


def cleanAndWriteSpeeches(fileinfos):
    """
    Go through files represented by dictionaries, create a record for each in the db, and save clean version of it[file].
    :param fileinfos:
    :return:
    """
    print "starting with {0} speeches".format(len(fileinfos))
    nrOfLongEnoughSpeeches = 0
    isPositiveVoteChunk = fileinfos[0]["vote"]
    for currFile in fileinfos:
        success = manager.insertSpeech(filename=currFile["filename"],
                                       vote = isPositiveVoteChunk,
                                       party = currFile["party"],
                                       mentionType=currFile["mention_type"] )
        if success:
            newFileContent = ""

            #with open(DIR_CLEANED_FILES + currFile["filename"], "w+") as writeH:
            with open("." + DIR_FILES + "/" + currFile["filename"], "r") as readH:
                wordsInArt = 0
                for line in readH:
                    for word in line.split():
                        cleanWord = cleaningOfWord(word)
                        if cleanWord:
                            wordsInArt += 1
                            newFileContent += cleanWord + " "
                if wordsInArt > 70:
                    nrOfLongEnoughSpeeches += 1
                    with open(DIR_CLEANED_FILES + currFile["filename"], "w+") as writeH:
                        writeH.seek(0)
                        writeH.write(newFileContent)
                        writeH.truncate()
        else:
            print "db error while saving {0}".format(currFile)
    print "{0} speeches ok".format(nrOfLongEnoughSpeeches)

def execute():
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

    cleanAndWriteSpeeches(posids)
    cleanAndWriteSpeeches(negids)

    stop = time.time()
    print "Time spent: ", stop-start


execute()