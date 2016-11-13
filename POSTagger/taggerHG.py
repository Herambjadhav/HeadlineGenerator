import nltk
import sys


def readFile(filePath):
    with open(filePath, 'r', encoding="latin1") as f:
        fileLines = f.read().splitlines()
        # text = word_tokenize("And now for something completely different")
        if(len(fileLines) > 0):
            summarizationText = fileLines[0]
            return summarizationText
        else:
            return None


def initTagger(filePath):
    if
    readFile(filePath)


if __name__ == "__main__":
    # Get the file path from command line
    # requires sys package
    # Sanity check for input filename
    if(len(sys.argv)>1):
        filePath = sys.argv[1]
    else:
        

    initTagger(filePath)




