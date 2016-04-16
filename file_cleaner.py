__author__ = 'Michal'

import multiprocessing
import time
from os import listdir, getcwd
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
    if wordBeingCleaned in [".", "?", "!"]:
        return wordBeingCleaned
    wordBeingCleaned = wordBeingCleaned.lower()
    wordBeingCleaned = re.sub('[^A-Za-z]+', '', wordBeingCleaned)
    if wordBeingCleaned in stopwords.words('english'):
        return None

    word = stemmer.stem(wordBeingCleaned).encode('ascii', 'english')
    return word if word != '' else None


def get_files_to_clean(dir):
    return filter(lambda x: x[0] != '.', sorted(listdir(dir)))

def cleanAndWriteSpeech(fileinfos):
    isPositiveVoteChunk = fileinfos[0]["vote"]
    for currFile in fileinfos:
        #lock.acquire()
        success = manager.insertSpeech(filename=currFile["filename"],
                                       vote = isPositiveVoteChunk,
                                       party = currFile["party"],
                                       mentionType=currFile["mention_type"] )
        #lock.release()
        if success:
            newFileContent = ""
            with open(DIR_CLEANED_FILES + currFile["filename"], "w+") as writeH:
                with open("." + DIR_FILES + "/" + currFile["filename"], "r") as readH:
                    for line in readH:
                        for word in line.split():
                            cleanWord = cleaningOfWord(word)
                            if cleanWord:
                                newFileContent += cleanWord + " "
                    writeH.seek(0)
                    writeH.write(newFileContent)
                    writeH.truncate()



    else:
        print "db error while saving {0}".format(currFile)

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

    listOfArticles = get_files_to_clean(getcwd() + DIR_FILES)
    lock = multiprocessing.Lock()
    processes = []

    cleanAndWriteSpeech(posids)
    cleanAndWriteSpeech(negids)

    # for chunk in [posids, negids]:
    #     process = multiprocessing.Process(target=cleanAndWriteSpeech, args=(chunk, lock))
    #     processes.append(process)
    #     process.start()
    #
    # for process in processes:
    #     process.join()

    stop = time.time()
    print "Time spent: ", stop-start