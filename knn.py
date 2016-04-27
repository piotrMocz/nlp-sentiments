from scipy.sparse import lil_matrix, csc_matrix
from config import DIR_CLEANED_NEWS, DIR_DUMP
from os import listdir
import pickle
import time
from db_manager import DBManager
K = 7


def loadData(directory):
    with open(directory + 'data.pkl', 'rb') as inputFile:
        data = pickle.load(inputFile)

    inputFile = open(directory + 'indices.pkl', 'rb')
    indices = pickle.load(inputFile)
    inputFile.close()

    inputFile = open(directory + 'indptr.pkl', 'rb')
    indptr = pickle.load(inputFile)
    inputFile.close()

    with open(directory + 'amountOfWords.pkl', 'rb') as inputFile:
        amountOfWords = pickle.load(inputFile)

    with open(directory + 'mapOfWords.pkl', 'rb') as inputFile:
        mapOfWords = pickle.load(inputFile)

    with open(directory + 'amountOfFiles.pkl', 'rb') as inputFile:
         amountOfFiles = pickle.load(inputFile)

    with open(directory + 'listOfArticleFiles.pkl', 'rb') as inputFile:
         listOfArticleFiles = pickle.load(inputFile)
    #
    # with open(directory + 'articleInvariants.pkl', 'rb') as inputFile:
    #     ngramsInvariants = pickle.load(inputFile)

    with open(directory + 'idfs.pkl', 'rb') as inputFile:
        idfs = pickle.load(inputFile)


    return csc_matrix((data, indices, indptr)), amountOfWords, mapOfWords, idfs, amountOfFiles, listOfArticleFiles

def createBagOfWordsFromNews(news, amountOfTerms, dictionary, idfs):
    bagOfWords = lil_matrix((1, amountOfTerms), dtype=float)
    indices = []
    for word in news:
        try:
            ind = dictionary[word]
            bagOfWords[0, ind] += idfs[ind]
            indices.append(ind)
        except:
            continue
    bagOfWords = csc_matrix(bagOfWords, dtype=float)
    return bagOfWords, indices

def corr(matrix, indices, vector,  amountOfDocuments):
    similarities = []
    for x in xrange(amountOfDocuments):
        simil =vector.dot(matrix[:, x])[0]
        similarities.append((x, simil))
    return sorted(similarities, key=lambda tup: tup[1], reverse=True)[:K]

if __name__ == "__main__":
    listOfArticles = filter(lambda x: x[0] != '.',sorted(listdir(DIR_CLEANED_NEWS)))
    start = time.time()
    print "started lading data..."
    mtx, amountOfWords, mapOfWords, idfs, amountOfFiles, newsList = loadData(DIR_DUMP)
    print "loaded data, took: {0}".format(time.time() - start)
    dbMan = DBManager()
    reut = []
    telegraph = []
    zeroH = []
    for fileName in listOfArticles[:20]:
        bowForFile, indices = createBagOfWordsFromNews(open(DIR_CLEANED_NEWS + fileName).read().replace('\n', ''),
                                              amountOfWords,
                                              mapOfWords,
                                              idfs)
       # print indices
        correlation = corr(mtx, indices, bowForFile, amountOfFiles)
        ans = []
        for el in correlation:
            ans.append(str(dbMan.getVote(newsList[el[0]])))
        isTrue = ans.count("T") > 2
        print ans
        if "routers" in fileName:
            reut.append(isTrue)
        elif "tele" in fileName:
            telegraph.append(isTrue)
        else:
            zeroH.append(isTrue)
    print telegraph
    print telegraph.count(True)/len(telegraph)
    print reut
    print reut.count(True)/len(reut)
    print zeroH
    print zeroH.count(True)/len(zeroH)


