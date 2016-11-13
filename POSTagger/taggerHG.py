import nltk
import sys


def readFile(filePath):
    with open(filePath, 'r', encoding="latin1") as f:
        # Open file and read Lines
        fileLines = f.read().splitlines()

        # Check if text file is not empty
        if(len(fileLines) > 0):
            # TO DO - confirm how many lines of the summarized text are to be considered?
            summarizedText = fileLines[0]
            return summarizedText
        else:
            return None


def extractNounPhrasesFromTree(tokenTree):
    g= "S"

def initTagger(filePath):
    if(filePath):
        summarizedText = readFile(filePath)
        if(not summarizedText is None):
            # split the input text into tokens
            tokens = nltk.word_tokenize(summarizedText,language='english')

            # perform POS Tagging on the tokens
            posTokens = nltk.pos_tag(tokens)

            # pattern to recognize noun phrases
            pattern = "NP: {<DT>?<JJ>*<NN>*<NNP>*<NNS>*}"
            # pattern = "NP: { < DT | PP\$ > ? < JJ > * < NN >}{ < NNP > +}{ < NN > +}"

            # create chunk parser
            NPChunker = nltk.RegexpParser(pattern)

            # parse the sentences of tokens
            result = NPChunker.parse(posTokens)

            extractNounPhrasesFromTree(result)
            g = "S"
        else:
            return "No text in input file"

if __name__ == "__main__":
    # Get the file path from command line
    # requires sys package
    # Sanity check for input filename
    if(len(sys.argv)>1):
        # filePath = sys.argv[1]
        filePath = "sum_test3.txt"
    else:
        print("Error file not found. Please check that the file exists\n")
        print("File path to be specified as input command line argument\n")
        exit(0)

    initTagger(filePath)




