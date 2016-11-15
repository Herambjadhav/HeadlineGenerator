import nltk
import sys
from collections import defaultdict
from HelperClasses.tree import Tree

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


def dictToList(inputDict):
    outputList = list()
    listLength = len(inputDict)
    i = 0
    count = listLength
    while(count > 0):
        if(i in inputDict.keys()):
            count -= 1
            outputList.append((i,inputDict[i]))
        i += 1
    return outputList

def possibleHeadlines(orderedSet):

    orderedList = dictToList(orderedSet)

    sentenceTree = Tree()

    sentenceTree.add_node("ROOT")
    parentReference = sentenceTree.nodes['ROOT'].identifier
    parentsReferenceList = list()
    parentsVerbReferenceList = list()
    # eachNode is a tuple where
    # tuple[0] is the type of phrase
    # tuple[1] is the Tree of the POS Tagger
    for eachNode in orderedList:

        if(eachNode[1][0] == "NP"):

            childID = str(eachNode[0])
            sentenceTree.add_node(childID,parentReference)
            parentsReferenceList.append(childID)

        if(eachNode[1][0] == "V"):

            for eachNodeparent in parentsReferenceList:
                childID = str(eachNode[0])
                sentenceTree.add_node(childID,eachNodeparent)
                parentsVerbReferenceList.append(childID)
            parentsReferenceList = []
        # print("TEST")

    possibleHeadlines = list()

    print(orderedSet)

def getMainVerb(verbPhrase):
    verbs = []
    for eachnode in verbPhrase:
        if(hasattr(eachnode,"_label")):
            if(eachnode._label == "V"):
                verbs.append(eachnode[0])
                return verbs
    return None

def getNNPNode(nodeList):
    NPNodeList = list()

    for eachnode in nodeList:
        if(hasattr(eachnode,"_label")):
            if(eachnode._label == "NP"):
                for nodes in eachnode:
                    if(nodes[1] == 'NNP' or nodes[1] == 'NNPS'):
                        NPNodeList.add(eachnode)

    if(NPNodeList):
        return (NPNodeList)
    else:
        return None

def getSingleNNPNode(nodeList):
    NPNodeList = list()

    for eachnode in nodeList:
        if(hasattr(eachnode,"_label")):
            if(eachnode._label == "NP"):
                for nodes in eachnode:
                    if(nodes[1] == 'NNP' or nodes[1] == 'NNPS'):
                        NPNodeList.append(eachnode)
                        return (NPNodeList)
    return None


def makePossibleHeadlines(result):

    orderedSubset = dict()

    NNPList = []

    ignoreIndex = []



    # Remove preposed adjuncts based on commas
    treeLength = len(result)
    for nodeIndex in range(0,treeLength):
        # Check if its not a sub tree
        if(not hasattr(result[nodeIndex],"_label")):
            if(result[nodeIndex][0] == ','):
                nodeList = [result[nodeIndex - 1],result[nodeIndex + 1]]
                NNPNodes = getNNPNode(nodeList)
                if(NNPNodes):
                    orderedSubset[nodeIndex] = ('NP',NNPNodes)
                    NNPList += NNPNodes

    # Complex NP not found pick up simple NP
    if(len(NNPList) == 0):
        for nodeIndex in range(0, treeLength):
            if (hasattr(result[nodeIndex], "_label")):
                NNPNodes = getSingleNNPNode([result[nodeIndex]])
                if(NNPNodes):
                    orderedSubset[nodeIndex] = ('NP', NNPNodes)
                    NNPList += NNPNodes



    #Get the verb (Predicates) that join Subject and Object
    for nodeIndex in range(0, treeLength):
        if(hasattr(result[nodeIndex],"_label")):
            if(result[nodeIndex]._label == 'VP'):
                mainverbs = getMainVerb(result[nodeIndex])
                orderedSubset[nodeIndex] = ('V',mainverbs)





    return orderedSubset




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

            # resultNP.draw()
            orderedSubset = makePossibleHeadlines(resultNP)
            possibleHeadlines(orderedSubset)
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

    filePath = "Data/sum_test19.txt"
    initTagger(filePath)

    # filePath = "Data/sum_test2.txt"
    # initTagger(filePath)

    # filePath = "Data/sum_test3.txt"
    # initTagger(filePath)




