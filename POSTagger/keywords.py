import nltk
import sys
import operator
from nltk.corpus import stopwords
import string


def readFile(filePath):
    with open(filePath, 'r', encoding="latin1") as f:
        # Open file and read Lines
        fileLines = f.read().splitlines()
        fileText = ''
        # Check if text file is not empty
        if(len(fileLines) > 0):
            # TO DO - confirm how many lines of the summarized text are to be considered?
            fileText += ' '.join(fileLines)

            return fileText
        else:
            return None


def getTokenFrequency(tokens):
    wordCounter =  dict()
    for word in tokens:
        if (word in wordCounter.keys()):
            wordCounter[word] += 1
        else:
            wordCounter[word] = 1

    sortedkeywords = sorted(wordCounter.items(), key=operator.itemgetter(1), reverse=True)
    print (sortedkeywords)

def initKeywords(filePath):
    if(filePath):
        articleText = readFile(filePath)
        if(not articleText is None):

            # Get the list of stopwords and insignificant words
            insignificantKeyWords = stopwords.words("english")
            insignificantKeyWords += [',', '.', 'I', 'said']

            # Get only ascii characters
            printable = set(string.printable)

            # check if the word is a stopword
            # if it is not in the stopword set add it list
            # combine list elements to form the string
            articleText = ' '.join([word for word in articleText.split() if word not in insignificantKeyWords])
            articleText = ''.join(filter(lambda x: x in printable, articleText))

            # split the input text into tokens
            tokens = nltk.word_tokenize(articleText ,language='english')
            getTokenFrequency(tokens)
        else:
            return "No text in input file"

if __name__ == "__main__":
    # Get the file path from command line
    # requires sys package
    # Sanity check for input filename
    if(len(sys.argv)>1):
        # filePath = sys.argv[1]
        filePath = "Data/test1.txt"
    else:
        print("Error file not found. Please check that the file exists\n")
        print("File path to be specified as input command line argument\n")
        exit(0)

    initKeywords(filePath)




