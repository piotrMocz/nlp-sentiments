from file_cleaner import cleaningOfWord
from config import DIR_NEWS, DIR_CLEANED_NEWS
import time
from os import listdir



def cleanArticles(listOfFilenames):
    for currFileName in listOfFilenames:
        newFileContent = ""
        with open(DIR_CLEANED_NEWS + currFileName, "w+") as writeH:
                with open(DIR_NEWS +  currFileName, "r") as readH:
                    for line in readH:
                        for word in line.split():
                            cleanWord = cleaningOfWord(word)
                            if cleanWord:
                                newFileContent += cleanWord + " "
                    writeH.seek(0)
                    writeH.write(newFileContent)
                    writeH.truncate()


if __name__ == "__main__":
    start = time.time()
    listOfArticles = filter(lambda x: x[0] != '.',sorted(listdir(DIR_NEWS)))
    print "number of articles found: {0}".format(len(listOfArticles))



# sometimes one news is crawled several times
    titles = set()
    distinctiveNews = set()
    for currFileName in listOfArticles:
        with open(DIR_NEWS + currFileName, "r") as readH:
            readH.readline()
            title = readH.readline()
            if not title in titles:
                titles.add(title)
                distinctiveNews.add(currFileName)
    stop = time.time()

    print len(titles)
    cleanArticles(distinctiveNews)
    print "Time spent: ", stop-start