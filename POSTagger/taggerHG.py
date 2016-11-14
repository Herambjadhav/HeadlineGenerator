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


def getNNPNode(nodeList):
    NPNodeList = list()

    for eachnode in nodeList:
        if(hasattr(eachnode,"_label")):
            if(eachnode._label == "NP"):
                for nodes in eachnode:
                    if(nodes[1] == 'NNP' or nodes[1] == 'NNPS'):
                        NPNodeList.append(eachnode)

    if(NPNodeList):
        return (NPNodeList)
    else:
        return None


def makePossibleHeadlines(result):

    summarizedTreeNodes = []

    # Remove preposed adjuncts based on commas
    treeLength = len(result)
    for nodeIndex in range(0,treeLength):
        # Check if its not a sub tree
        if(not hasattr(result[nodeIndex],"_label")):
            if(result[nodeIndex][0] == ','):
                nodeList = [result[nodeIndex - 1],result[nodeIndex + 1]]
                NNPNodes = getNNPNode(nodeList)
                if(NNPNodes):
                    summarizedTreeNodes += NNPNodes



    print(summarizedTreeNodes)




def getDescribersCommas(tokens):
    commaList= list()
    commaIndex = 0
    for eachtoken in tokens:
        if("," in eachtoken):
            # Check if the comma is used to describe
            # and not used as a punctuation to list a set of things
            # eg red, green and blue

            commaIndex += 1

def initTagger(filePath):
    if(filePath):
        summarizedText = readFile(filePath)
        if(not summarizedText is None):
            # split the input text into tokens
            tokens = nltk.word_tokenize(summarizedText,language='english')

            # perform POS Tagging on the tokens
            posTokens = nltk.pos_tag(tokens)




            # pattern to recognize noun phrases
            patternNP = "NP: {<DT>?<JJ>*<NN>*<NNP>*<NNS>*}"
            # patternVP = "VP: {<VBN>(<DT>?<JJ>*<NN>*<NNP>*<NNS>*<IN>*)}"


            # pattern = "NP: { < DT | PP\$ > ? < JJ > * < NN >}{ < NNP > +}{ < NN > +}"

            # create chunk parser
            # NPChunker = nltk.RegexpParser(patternNP)
            NPChunker = nltk.RegexpParser('''
                            NP: {<DT>? <JJ>* <NN>* <NNP>* <NNS>* <PP>*} # NP modified
                            P: {<IN>}           # Preposition
                            V: {<V.*>}          # Verb
                            PP: {<P> <NP>}      # PP -> P NP
                            VP: {<V> <NP|PP>*}  # VP -> V (NP|PP)*
                            ''')
            # VPChunker = nltk.RegexpParser(patternVP)

            # parse the sentences of tokens
            resultNP = NPChunker.parse(posTokens)
            # resultVP = VPChunker.parse(posTokens)


            makePossibleHeadlines(resultNP)
        else:
            return "No text in input file"

if __name__ == "__main__":
    # Get the file path from command line
    # requires sys package
    # Sanity check for input filename
    filePath = "Data/sum_test3.txt"

    # if(len(sys.argv)>1):
    #     filePath = sys.argv[1]
    #     filePath = "Data/sum_test1.txt"
    # else:
    #     print("Error file not found. Please check that the file exists\n")
    #     print("File path to be specified as input command line argument\n")
    #     exit(0)

    filePath = "Data/sum_test1.txt"
    initTagger(filePath)

    filePath = "Data/sum_test2.txt"
    initTagger(filePath)

    filePath = "Data/sum_test3.txt"
    initTagger(filePath)




