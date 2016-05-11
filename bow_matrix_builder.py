import os
import time
import numpy
import math
import scipy
import pickle
import scipy.sparse

from config import DIR_CLEANED_FILES, DIR_DUMP


def writeDataToFile(matrix, dictOfThingsToDump, path):
    """

    :param matrix: the main matrix
    :param dictOfThingsToDump: mapping (nameOfFileToWrite) -> (content)
    """

    mat = scipy.sparse.csc_matrix(matrix)

    with open(path + 'data.pkl', 'wb') as output:
        pickle.dump(mat.data, output)

    with open(path + 'indices.pkl', 'wb') as output:
        pickle.dump(mat.indices, output)

    with open(path + 'indptr.pkl', 'wb') as output:
        pickle.dump(mat.indptr, output)

    for x in dictOfThingsToDump.keys():
        with open(path + x + '.pkl', 'wb') as output:
            pickle.dump(dictOfThingsToDump[x], output)


def normalization(matrix, amountOfDocuments):
    """
    Function applying normalization to the main matrix
    :param matrix: s.e.
    :param amountOfDocuments:s.e.
    :return: modified matrix
    """

    matrixSparse = scipy.sparse.csc_matrix(matrix)

    nonzeroIndices = matrixSparse.nonzero()
    firstList = nonzeroIndices[0]
    secondList = nonzeroIndices[1]
    amountOfNonZeroCells = len(firstList)
    sumList = [0 for x in xrange(amountOfDocuments)]

    for cellIndex in xrange(amountOfNonZeroCells):
        sumList[secondList[cellIndex]] += matrix[firstList[cellIndex], secondList[cellIndex]]**2

    for x in xrange(len(sumList)):
        sumList[x] = math.sqrt(sumList[x])

    for cellInd in xrange(amountOfNonZeroCells):
        matrix[firstList[cellInd], secondList[cellInd]] /= sumList[secondList[cellInd]]


    return matrix

def idf(matrix, numberOfArticles, dictOfTermOccurrences, listOfWords):
    """
    Function applying idf to the main matrix.
    :param matrix: the main matrix
    :param numberOfArticles: s.e.
    :param dictOfTermOccurrences: mapping (term) -> (amounfOfDocsWithTerm)
    :param listOfWords: all words
    :return: modified matrix, list of idf values
    """

    idfs = []
    for ind, word in enumerate(listOfWords):
        amountOfDocumentsWithGivenTerm = dictOfTermOccurrences[word]
        idf = math.log(float(numberOfArticles)/float(amountOfDocumentsWithGivenTerm), 10)
        matrix[ind,:] *= idf
        idfs.append(idf)
    return matrix, idfs

def gatherAllWordsFromArticles(listOfArticles, pathToArticles):
    """
    Gather all words from a given list of articles.
    Opened files format: [pathToArticles + x for x in listOfArticles]

    :param listOfArticles: list of article names
    :param pathToArticles: directory with articles
    :return:    words - set of all words,
                dictOfWords - mapping (word) -> (word's id)
                matrix - bag of words
                dictOfTermOccurrences -
    """

    wordAmount = 0
    words = set()
    dictOfWords = dict()
    dictOfTermOccurrences = dict()

    workingListOfOccurrences = []
    mapOfWords = []
    for currentFileName in listOfArticles:
        with open(os.path.join(pathToArticles, currentFileName)) as currentFile:
            indexesOfWordsInCurrentFile = []
            for word in currentFile.read().split():
                    if word in words:
                        indexesOfWordsInCurrentFile.append(dictOfWords[word])
                    else:
                        dictOfTermOccurrences[word] = 1
                        words.add(word)
                        dictOfWords[word] = wordAmount
                        mapOfWords.append(word)
                        indexesOfWordsInCurrentFile.append(wordAmount)
                        wordAmount += 1

            workingListOfOccurrences.append(indexesOfWordsInCurrentFile)


    matrix = numpy.zeros((len(words), len(listOfArticles)), float)

    for x, obj in enumerate(workingListOfOccurrences):
        for index in obj:
            matrix[index,x] += 1
        for index in set(obj):
            dictOfTermOccurrences[mapOfWords[index]] += 1

    return words, dictOfWords, matrix, dictOfTermOccurrences, mapOfWords


if __name__ == '__main__':
    listOfCleanedArticles = filter(lambda x: x[0] != '.', sorted(os.listdir(DIR_CLEANED_FILES)))
    amountOfFiles = len(listOfCleanedArticles)

    print "Amount of files: ", amountOfFiles

    start = time.time()
    setOfWords, mapOfWords, matrix, dictOfTermOccurrences, listOfWords = gatherAllWordsFromArticles(listOfCleanedArticles, DIR_CLEANED_FILES)
    stop = time.time()

    print "Gathering words done, took: ", stop-start, " seconds"
    print "Amount of words: ", len(setOfWords), "\n"

    start = time.time()
    matrix, idfs = idf(matrix, amountOfFiles, dictOfTermOccurrences, listOfWords)
    stop = time.time()

    print "IDF done, took : ", stop-start, " seconds\n"

    start = time.time()
    matrix = normalization(matrix, amountOfFiles)
    stop = time.time()

    print "Normalization done, took: ", stop-start, " seconds\n"

    start = time.time()
    writeDataToFile(matrix, { "amountOfWords" : len(setOfWords),
                              "mapOfWords" : mapOfWords,
                              "amountOfFiles" :  amountOfFiles,
                              "dictOfTermOccurrences" : dictOfTermOccurrences,
                              "listOfArticleFiles" : listOfCleanedArticles,
                              "idfs" : idfs
                            },
                    path = DIR_DUMP)

    stop = time.time()

    print "Writing to file done, took: ", stop - start, " seconds\n"